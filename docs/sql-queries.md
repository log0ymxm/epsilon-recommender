
## Find Average IGN Rating

    SELECT
    AVG(CAST(coalesce(NULLIF(regexp_replace(vga.value, '[ \t\n\r]*', '', 'g'), 'None'), '0') AS float)),
    max(CAST(coalesce(NULLIF(regexp_replace(vga.value, '[ \t\n\r]*', '', 'g'), 'None'), '0') AS float)),
    min(CAST(coalesce(NULLIF(regexp_replace(vga.value, '[ \t\n\r]*', '', 'g'), 'None'), '0') AS float))
    FROM "recommender_videogameattribute" AS vga

    JOIN "attributes_attributeoption" AS o ON o.id = vga.option_id
    JOIN "recommender_videogame" AS vg ON vg.id = vga.video_game_id

    WHERE o.name LIKE 'ign_rating'
