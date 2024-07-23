def print_results(G, roundList):

    dataList = []   #list of matchup data to be printed and viewed
    scoreRatingDiffList = [] #list of score and rating differences among all matchups
    sdDict = {} #dict containing all the score differences as keys and the number of occurences as values
    sameSchoolNum = 0
    for pairs in roundList:
        for (j,k) in pairs:
            if G.nodes[j]['school'] == G.nodes[k]['school']:
                sameSchoolNum += 1
                
            scoreDiff = abs(G.nodes[j]['score'] - G.nodes[k]['score'])
            ratingDiff = abs(G.nodes[j]['rating'] - G.nodes[k]['rating'])
            scoreRatingDiffList.append((scoreDiff, ratingDiff))
            if scoreDiff in sdDict:
                sdDict[scoreDiff] += 1
            else:
                sdDict[scoreDiff] = 1
            print(ratingDiff)