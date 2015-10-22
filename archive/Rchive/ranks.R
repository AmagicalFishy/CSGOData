library(RMySQL)
library(MASS)
library(ggplot2)
library(hexbin)
library(mgcv)
library(Cairo)

# Connect to SQL Database
con = dbConnect(MySQL(), user='root', password='password',
                dbname='csgo', host='localhost')

# Get data from table
dbListTables(con)
dbListFields(con, 'csgo_matches')
query = dbSendQuery(con, "select * from csgo_matches")
dat = fetch(query, n = -1)

# Put data into convenient variables
cs_score1 = dat[4]
cs_rank1 = dat[5]
cs_score2 = dat[7]
cs_rank2 = dat[8]

# Rank differences and score differences in each match
# Positive rank means Team 1 is higher in rank
# Positive score means Team 1 won
rankDiff = cs_rank1 - cs_rank2
rankDiff = unlist(rankDiff)
scoreDiff = cs_score1 - cs_score2
scoreDiff = unlist(scoreDiff)

# Dataframe of above differences
df <- data.frame(x = rankDiff, y = scoreDiff)

# Save file as .png
Cairo(file="scorerankvis.png", type="png", 
    width=1000, height=1000, dpi=72, 
    pointsize=30)

# Plot density map
ggplot(df,aes(x, y)) + stat_binhex(bins=30) + # Hex-bin fill
guides(fill = guide_colorbar(barheight = 20)) + # Colorbar config.
    scale_fill_gradient(low="blue", high="white", space="Lab") +
    # Axis labels! (What a mess)
    xlab("Team 1 Lower                    Rank Difference                     Team 2 Lower") + 
    ylab("Team 2 Wins                    Score Difference                     Team 1 Wins") + 
    ggtitle("CS:GO\nGame Score vs. Rank Visualization") + # Title
    scale_y_continuous(breaks=seq(-15,15,3)) + # y-ticks
    scale_x_continuous(breaks=seq(-2,2,.50)) + # x-ticks
    theme(panel.background = element_rect(fill = 'grey'), # Gray BG
          # Axis Text
          plot.title = element_text(color="#666666", face="bold", 
                                    size=40, hjust=0), 
          axis.title = element_text(color="#666666", face="bold", 
                                    size=25))
dev.off() 

# Fetch new data
for (ii in 1:2) {
    queryText = paste("SELECT t1score, t2score, t1rank, t2rank FROM csgo_matches WHERE",
    "(t1rank >=", ii*.25 - .25, "AND t1rank <", ii*.25, ")")
    query = dbSendQuery(con, queryText)
    dat1 = fetch(query, n = -1)

    queryText = paste("SELECT t2score, t1score, t2rank, t1rank FROM csgo_matches WHERE",
        "(t2rank >=", ii*.25 - .25, "AND t2rank <", ii*.25, ")")
    query = dbSendQuery(con, queryText)
    dat2 = fetch(query, n = -1)

    homeRank1 = unlist(dat1[3])
    homeRank2 = unlist(dat2[3])
    homeScore1 = unlist(dat1[1])
    homeScore2 = unlist(dat2[1])
    awayRank1 = unlist(dat1[4])
    awayRank2 = unlist(dat2[4])
    awayScore1 = unlist(dat1[2])
    awayScore2 = unlist(dat2[2])

    homeRank = c(homeRank1, homeRank2)
    homeScore = c(homeScore1, homeScore2)
    awayRank = c(awayRank1, awayRank2)
    awayScore = c(awayScore1, awayScore2)

df <- data.frame(homeRank, awayRank, homeScore, awayScore)
df
}
