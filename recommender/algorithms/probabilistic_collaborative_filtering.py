from collections import defaultdict
import math
from recommends.converters import convert_vote_list_to_userprefs, convert_vote_list_to_itemprefs
from recommends.algorithms.base import BaseAlgorithm

import numpy as np
import theano.tensor as T
import theano
import scipy.stats as stats
from recommends.converters import convert_vote_list_to_userprefs, convert_vote_list_to_itemprefs
from sklearn.preprocessing import OneHotEncoder
from recommender.models import VideoGame

@staticmethod
def sim_distance(p1, p2):
    """Returns a distance-based similarity score for p1 and p2"""
    # Get the list of shared_items
    #print '-- sim_distance', p1, p2
    si = [item for item in p1 if item in p2]

    if len(si) != 0:
        squares = [pow(p1[item] - p2[item], 2) for item in si]
        # Add up the squares of all the differences
        sum_of_squares = sum(squares)
        return 1 / (1 + np.sqrt(sum_of_squares))
    return 0

class ProbabilisticMatrixFactorizationAlgorithm(BaseAlgorithm):
    """
    """
    similarity = sim_distance

    def top_matches(self, prefs, p1):
        """
        Returns the best matches for p1 from the prefs dictionary.
        """
        #print 'top_matches', prefs, p1
        #print '\n'
        return [(p2, self.similarity(prefs[p1], prefs[p2])) for p2 in prefs if p2 != p1]

    def matrix_factorization(self, R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
        print 'matrix factorization'
        Q = Q.T

        for step in xrange(steps):

            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if R[i][j] > 0:
                        eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                        for k in xrange(K):
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            eR = np.dot(P,Q)
            e = 0

            for i in xrange(len(R)):
                for j in xrange(len(R[i])):

                    if R[i][j] > 0:

                        # sum
                        e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)

                        # sum
                        for k in xrange(K):
                            e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))

            # our minimum error rate has reached some lower bounds, stop
            if e < 0.001:
                break
        return P, Q.T

    def calculate_similarities(self, vote_list, verbose=0):
        #print "--------------------------------------------------"
        #print "calculate_similarities"
        #print "--------------------------------------------------"

        # vote_list
        # [
        #     ("<user1>", "<object_identifier1>", <score>),
        #     ("<user1>", "<object_identifier2>", <score>),
        # ]

        # Invert the preference matrix to be item-centric
        itemPrefs = convert_vote_list_to_itemprefs(vote_list)

        itemMatch = {}

        for item in itemPrefs:
            # Find the most similar items to this one
            itemMatch[item] = self.top_matches(itemPrefs, item)

        iteritems = itemMatch.items()

        # returns
        # [
        #     ("<object_identifier1>", [
        #                     (<related_object_identifier2>, <score>),
        #                     (<related_object_identifier3>, <score>),
        #     ]),
        #     ("<object_identifier2>", [
        #                     (<related_object_identifier2>, <score>),
        #                     (<related_object_identifier3>, <score>),
        #     ]),
        # ]


        return iteritems

    def calculate_recommendations(self, vote_list, itemMatch, itemIgnored):
        """
        ``itemMatch`` is supposed to be the result of ``calculate_similarities()``

        Returns a list of recommendations:

        ::

            [
                (<user1>, [
                    ("<object_identifier1>", <score>),
                    ("<object_identifier2>", <score>),
                ]),
                (<user2>, [
                    ("<object_identifier1>", <score>),
                    ("<object_identifier2>", <score>),
                ]),
            ]

        """
        #print "--------------------------------------------------"
        #print "calculate_recommendations"
        #print "--------------------------------------------------"

        # http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/

        # U = np.array('users')
        # D = np.array('video_games')

        # R = |U| cross |D|

        # We want to discover K latent features

        # Find
        # P(a | |U| corss K matrix)
        # Q(a | |D| cross K matrix)
        # Such that their product approximates R
        # R approx= P cross transpose(Q) = hat(R)
        #

        # r[i][j] = transpose(p)[i] * q[j]
        #         = sum( 1..k, p[i][k] * q[k][j] )

        # e[i][j]**2 = (r[i][j] - hat(r)[i][j])**2
        #            = (r[i][j] - sum( 1..K, p[i][k] * q[k][j]))**2
        # squared error, estimated rating can be either higher or lower than the real thing

        # find the gradient
        # diff(e[i][j]**2, p[i][k]) = -2*(r[i][j] - hat(r)[i][j]) * (q[k][j]) = -2*e[i][j] * q[k][j]
        # diff(e[i][j]**2, q[k][j]) = -2*(r[i][j] - hat(r)[i][j]) * (p[i][k]) = -2*e[i][j] * p[i][k]

        # update rules
        # alpha = settings.alpha # learning_rate
        # alpha = 0.0002 # learning_rate
        # p[i][k]' = p[i][k] + alpha * diff(e[i][j]**2, p[i][k])
        #          = p[i][k] + 2 * alpha * e[i][j] * q[k][j]
        # q[k][j]' = q[k][j] + alpha * diff(e[i][j]**2, q[k][j])
        #          = q[k][j] + 2 * alpha * e[i][j] * p[i][k]

        # training data
        # T = (u[i], d[j], r[i][j])
        #     np.array()

        # iterate until convergance
        # E = sum((u[i], d[j], r[i][j]) in T, e[i][j])
        #   = sum((u[i], d[j], r[i][j]) in T, r[i][j]
        #     - sum(1..k, p[i][k]*q[k][j]))**2

        # regularization
        # beta = 0.02
        # e[i][j]**2 =     (r[i][j] - sum(1..K, p[i][j]*q[k][j]))**2
        #                  + ((beta/2) * sum(1..K, norm(P)**2 + norm(Q)**2))
        #
        # p[i][k]' = p[i][k] + alpha * (2 * e[i][j] * q[k][j] - beta * p[i][k])
        # q[k][j]' = q[k][j] + alpha * (2 * e[i][j] * p[i][k] - beta * q[k][j])

        data = np.array(vote_list)

        encoder = OneHotEncoder()

        users = data[:,0]
        unique_users = list(set(users))
        for i in range(len(users)):
          users[i] = unique_users.index(users[i])

        video_games = data[:,1]
        unique_games = list(set(video_games))
        for i in range(len(video_games)):
          video_games[i] = unique_games.index(video_games[i])

        ratings = data[:,2]
        M = len(set(video_games))
        N = len(set(users))
        R = np.zeros((N,M))
        for i in range(len(users)):
          user = users[i]
          game = video_games[i]
          rating = ratings[i]
          R[user][game] = rating

        K = 2

        P = np.random.rand(N,K)
        Q = np.random.rand(M,K)

        nP, nQ = self.matrix_factorization(R, P, Q, K)
        nR = np.dot(nP, nQ.T)

        itemMatch = {}
        for i in range(N):
          user = unique_users[i]
          itemMatch[user] = []
          for j in range(M):
            if R[i][j] == 0:
              video_game = unique_games[j]
              recommendation = (video_game, nR[i][j])
              itemMatch[user].append(recommendation)
        itemMatch[None] = []
        print 'pmf recommendations', itemMatch.items()
        print '\n'
        recommendations = itemMatch.items()

        # returns
        # [
        #     (<user1>, [
        #         ("<object_identifier1>", <score>),
        #         ("<object_identifier2>", <score>),
        #     ]),
        #     (<user2>, [
        #         ("<object_identifier1>", <score>),
        #         ("<object_identifier2>", <score>),
        #     ]),
        # ]

        return recommendations
