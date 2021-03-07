library(ggplot2)


data_mp = read.table('data_mp.txt', head=TRUE)

ggplot(data_mp, aes(iter, mp, group=lang, color=lang)) +
  geom_point(size=2.5, position=position_jitterdodge(jitter.width = 0.1, jitter.height=0.1)) +
  ggtitle("Minimal Pairs /f/-/ θ/ in the vocabulary")+
  geom_smooth() +
  xlab("Words learned") +
  ylab("Minimal Pairs") +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5))


data_syl = read.table('data_syl.txt', head=TRUE)

ggplot(data_syl, aes(iter, mp, group=lang, color=lang)) +
  geom_point(size=2.5, position=position_jitterdodge(jitter.width = 0.1, jitter.height=0.1)) +
  ggtitle("Word-initial CV contrasts between /f/-/θ/ in the vocabulary")+
  geom_smooth() +
  xlab("Words learned") +
  ylab("Syllable contrasts") +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5))



  

