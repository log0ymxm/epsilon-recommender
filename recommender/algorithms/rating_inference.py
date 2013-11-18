import numpy as np
import pymc as pm

# For ordering our video games, we want to estimate the "true" rating
# of a video game rather than the observed rating we have in our
# database. IE a game with 5 stars and 1 rating, might normally be
# sorted higher than a game with 4.9 stars and 200 ratings. But logically
# we know that the one with more ratings is probably more popular
# than the one with 1 rating.
#
# We can use bayesian inference to model this sorting problem, and
# estimate what the posterior (true) rating is based of our prior (observed)
# rating. The below function is a derived normal approximation based on
# finding the binomial likelihood with traditional bayesian inference.
#
# This idea is explored and the derived formula is based off the reddit
# sorting example found in the book chapter linked below
#
# http://nbviewer.ipython.org/urls/raw.github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/master/Chapter4_TheGreatestTheoremNeverTold/LawOfLargeNumbers.ipynb
#
# The function has been modified to work with a numerical rating setup (1-5)
# rather than the upvote/downvote example found in the book.
#
# After approximating the true rating, we subtract the standard error to
# obtain a lower bounds rating value which we then choose to order by.
def intervals(vote_sum, number_of_votes):
    a = 1. + vote_sum
    b = 1. - (number_of_votes - vote_sum)
    mu = a/(a+b)
    std_err = 1.65*np.sqrt( (a*b)/( (a+b)**2*(a+b+1.) ) )
    return ( mu, std_err )

def posterior_upvote_ratio( vote_sum, number_of_votes, samples = 20000):
    """
    This function accepts the number of upvotes and downvotes a particular comment recieved,
    and the number of posterior samples to return to the user. Assumes a uniform prior.
    """
    N = upvotes + downvotes
    upvote_ratio = pm.Uniform( "upvote_ratio", 0, 1 )
    #observations = pm.Binomial( "obs",  N, upvote_ratio, value = upvotes, observed = True)
    observations = pm.Binomial( "obs",  number_of_votes, upvote_ratio, value = votes_sum, observed = True)
    #do the fitting; first do a MAP as it is cheap and useful.
    map_ = pm.MAP([upvote_ratio, observations ]).fit()
    mcmc = pm.MCMC([upvote_ratio, observations ])
    mcmc.sample(samples, samples/4)
    return mcmc.trace("upvote_ratio")[:]
