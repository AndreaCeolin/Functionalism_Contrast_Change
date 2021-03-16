library(tidyverse)
library(ggsignif)

###########################################################
#4.4 Perception and Production in phonological development


###########################################################
# /t/

Eng_t = c(rep.int(1,453), rep.int(0,117))
Grk_t = c(rep.int(1,468), rep.int(0,126))
Chi_t= c(rep.int(1,420), rep.int(0,255))
Jap_t= c(rep.int(1,338), rep.int(0,165))
#-39
#Jap_t_rev= c(rep.int(1,299), rep.int(0,126))

accuracy_t = c(sum(Eng_t)/length(Eng_t), sum(Grk_t)/length(Grk_t), sum(Chi_t)/length(Chi_t), sum(Jap_t)/length(Jap_t))

S = data_frame(Language=factor(c('English', 'Greek', 'Cantonese', 'Japanese'), levels=c('English', 'Greek', 'Cantonese', 'Japanese')), Accuracy=accuracy_t)

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of t-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("Greek", "Cantonese")), annotations = '**', size=1, margin_top=0.05, tip_length=0.1) +
  geom_signif(comparisons = list(c("English", "Japanese")), annotations = '**', size=1, margin_top=0.99, tip_length=0.1) +
  geom_signif(comparisons = list(c("Greek", "Japanese")), annotations = '**', size=1, margin_top=0.33, tip_length=0.1) +
  geom_signif(comparisons = list(c("English", "Cantonese")), annotations = '**', size=1, margin_top=0.7, tip_length=0.1) +
  xlab('')


wilcox.test(Eng_t, Grk_t)
wilcox.test(Eng_t, Jap_t)
wilcox.test(Eng_t, Chi_t)
wilcox.test(Grk_t, Jap_t)
wilcox.test(Grk_t, Chi_t)
wilcox.test(Jap_t, Chi_t)


prop.test(c(sum(Eng_t), sum(Grk_t)), c(length(Eng_t), length(Grk_t)), correct=FALSE)
prop.test(c(sum(Eng_t), sum(Jap_t)), c(length(Eng_t), length(Jap_t)), correct=FALSE)
prop.test(c(sum(Eng_t), sum(Chi_t)), c(length(Eng_t), length(Chi_t)), correct=FALSE)
prop.test(c(sum(Grk_t), sum(Chi_t)), c(length(Grk_t), length(Chi_t)), correct=FALSE)
prop.test(c(sum(Grk_t), sum(Jap_t)), c(length(Grk_t), length(Jap_t)), correct=FALSE)
prop.test(c(sum(Jap_t), sum(Chi_t)), c(length(Jap_t), length(Chi_t)), correct=FALSE)

###########################################################
# /d/

Eng_d = c(rep.int(1,444), rep.int(0,122))
Jap_d = c(rep.int(1,193), rep.int(0,181))


wilcox.test(Eng_d, Jap_d)
prop.test(c(sum(Eng_d), sum(Jap_d)), c(length(Eng_d), length(Jap_d)), correct=FALSE)

accuracy_d = c(sum(Eng_d)/length(Eng_d), sum(Jap_d)/length(Jap_d))

S = data_frame(Language=c('English', 'Japanese'),Accuracy=accuracy_d)

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of d-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("English", "Japanese")), annotations = '**', size=1, margin_top=0.3, tip_length=0.2) +
  xlab('')


###########################################################
# /k/
  
Eng_k = c(rep.int(1,477), rep.int(0,93))
Grk_k = c(rep.int(1,262), rep.int(0,110))
Chi_k= c(rep.int(1,370), rep.int(0,198))
Jap_k= c(rep.int(1,383), rep.int(0,88))


wilcox.test(Eng_k, Grk_k)
wilcox.test(Eng_k, Jap_k)
wilcox.test(Eng_k, Chi_k)
wilcox.test(Grk_k, Jap_k)
wilcox.test(Grk_k, Chi_k)
wilcox.test(Jap_k, Chi_k)

prop.test(c(sum(Eng_k), sum(Grk_k)), c(length(Eng_k), length(Grk_k)), correct=FALSE)
prop.test(c(sum(Eng_k), sum(Jap_k)), c(length(Eng_k), length(Jap_k)), correct=FALSE)
prop.test(c(sum(Eng_k), sum(Chi_k)), c(length(Eng_k), length(Chi_k)), correct=FALSE)
prop.test(c(sum(Grk_k), sum(Chi_k)), c(length(Grk_k), length(Chi_k)), correct=FALSE)
prop.test(c(sum(Grk_k), sum(Jap_k)), c(length(Grk_k), length(Jap_k)), correct=FALSE)
prop.test(c(sum(Jap_k), sum(Chi_k)), c(length(Jap_k), length(Chi_k)), correct=FALSE)


accuracy_k = c(sum(Eng_k)/length(Eng_k), sum(Grk_k)/length(Grk_k), sum(Chi_k)/length(Chi_k), sum(Jap_k)/length(Jap_k))

barplot(accuracy_k, names.arg=c('Eng', 'Grk', 'Can', 'Jap'), main='Accuracy of k-production', ylim=c(0,1))

S = data_frame(Language=factor(c('English', 'Greek', 'Cantonese', 'Japanese'), levels=c('English', 'Greek', 'Cantonese', 'Japanese')), Accuracy=accuracy_k)

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of k-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("Japanese", "Cantonese")), annotations = '**', size=1, margin_top=0.05, tip_length=0.1) +
  geom_signif(comparisons = list(c("English", "Greek")), annotations = '**', size=1, margin_top=0.6, tip_length=0.1) +
  geom_signif(comparisons = list(c("Japanese", "Greek")), annotations = '**', size=1, margin_top=0.33, tip_length=0.1) +
  geom_signif(comparisons = list(c("English", "Cantonese")), annotations = '**', size=1, margin_top=0.99, tip_length=0.1) +
  xlab('')


###########################################################
# /g/

Eng_g = c(rep.int(1,173), rep.int(0,61))
Jap_g = c(rep.int(1,243), rep.int(0,231))

wilcox.test(Eng_g, Jap_g)

prop.test(c(sum(Eng_g), sum(Jap_g)), c(length(Eng_g), length(Jap_g)), correct=FALSE)


accuracy_g = c(sum(Eng_g)/length(Eng_g), sum(Jap_g)/length(Jap_g))

barplot(accuracy_g, names.arg=c('Eng', 'Jap'), main='Accuracy of g-production', ylim=c(0,0.6))

S = data_frame(Language=c('English', 'Japanese'),Accuracy=accuracy_g)

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of g-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("English", "Japanese")), annotations = '**', size=1, margin_top=0.3, tip_length=0.2) +
  xlab('')


###########################################################
# /s/

Eng_s = c(rep.int(1,265), rep.int(0,275))
Grk_s = c(rep.int(1,287), rep.int(0,320))
Jap_s= c(rep.int(1,143), rep.int(0,305))
Chi_s= c(rep.int(1,233), rep.int(0,190))


accuracy_s = c(sum(Eng_s)/length(Eng_s), sum(Grk_s)/length(Grk_s), sum(Chi_s)/length(Chi_s), sum(Jap_s)/length(Jap_s))

S = data_frame(Language=factor(c('English', 'Greek', 'Cantonese', 'Japanese'), levels=c('English', 'Greek', 'Cantonese', 'Japanese')), Accuracy=accuracy_s)

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of s-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("Greek", "Japanese")), annotations = '**', size=1, margin_top=0.55, tip_length=0.1) +
  geom_signif(comparisons = list(c("English", "Japanese")), annotations = '**', size=1, margin_top=0.75, tip_length=0.1) +
  geom_signif(comparisons = list(c("Cantonese", "Greek")), annotations = '*', size=1, margin_top=0.15, tip_length=0.1) +
  geom_signif(comparisons = list(c("Cantonese", "Japanese")), annotations = '**', size=1, margin_top=0.35, tip_length=0.1) +
  xlab('')

wilcox.test(Eng_s, Grk_s)
wilcox.test(Eng_s, Jap_s)
wilcox.test(Eng_s, Chi_s)
wilcox.test(Grk_s, Jap_s)
wilcox.test(Grk_s, Chi_s)
wilcox.test(Jap_s, Chi_s)

prop.test(c(sum(Eng_s), sum(Grk_s)), c(length(Eng_s), length(Grk_s)), correct=FALSE)
prop.test(c(sum(Eng_s), sum(Jap_s)), c(length(Eng_s), length(Jap_s)), correct=FALSE)
prop.test(c(sum(Eng_s), sum(Chi_s)), c(length(Eng_s), length(Chi_s)), correct=FALSE)
prop.test(c(sum(Grk_s), sum(Chi_s)), c(length(Grk_s), length(Chi_s)), correct=FALSE)
prop.test(c(sum(Grk_s), sum(Jap_t)), c(length(Grk_s), length(Jap_s)), correct=FALSE)
prop.test(c(sum(Jap_s), sum(Chi_s)), c(length(Jap_s), length(Chi_s)), correct=FALSE)


###########################################################
# /S/

Eng_S = c(rep.int(1,269), rep.int(0,259))
Jap_S= c(rep.int(1,171), rep.int(0,271))

wilcox.test(Eng_S, Jap_S)

prop.test(c(sum(Eng_S), sum(Jap_t)), c(length(Eng_S), length(Jap_S)), correct=FALSE)

accuracy_S = c(sum(Eng_S)/length(Eng_S), sum(Jap_S)/length(Jap_S))

barplot(accuracy_S, names.arg=c('Eng', 'Jap'), main='Accuracy of ʃ-production', ylim=c(0,0.6))

S = data_frame(Language=factor(c('English', 'Japanese'), levels=c('English', 'Japanese')),Accuracy=c(0.509, 0.387))

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of ʃ-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("English", "Japanese")), annotations = '**', size=1, margin_top=0.3, tip_length=0.2) +
  xlab('')


###########################################################
# /T/

Eng_T = c(rep.int(1,24), rep.int(0,84))
Grk_T= c(rep.int(1,40), rep.int(0,77))

wilcox.test(Eng_T, Grk_T)
prop.test(c(sum(Eng_T), sum(Grk_T)), c(length(Eng_T), length(Grk_T)), correct=FALSE)

accuracy_T = c(sum(Eng_T)/length(Eng_T), sum(Grk_T)/length(Grk_T))

barplot(accuracy_T, names.arg=c('Eng', 'Grk'), main='Accuracy of θ-production', ylim=c(0,0.6))

theta = data_frame(Language=factor(c('English', 'Greek'), levels=c('English', 'Greek')),Accuracy=c(0.222, 0.342))

ggplot(data=theta, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of θ-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14)) +
  geom_signif(comparisons = list(c("English", "Greek")), annotations = '*', size=1, margin_top=0.3, tip_length=0.2) +
  xlab('')


###########################################################
# /tS/

Eng_tS = c(rep.int(1,259), rep.int(0,261))
Jap_tS= c(rep.int(1,251), rep.int(0,204))
Eng2_tS = c(rep.int(1,478), rep.int(0,325))
Jap2_tS= c(rep.int(1,448), rep.int(0,237))


wilcox.test(Eng_tS, Jap_tS)
wilcox.test(Eng2_tS, Jap2_tS)

prop.test(c(sum(Eng_tS), sum(Jap_tS)), c(length(Eng_tS), length(Jap_tS)), correct=FALSE)


accuracy_tS = c(sum(Eng_tS)/length(Eng_tS), sum(Jap_tS)/length(Jap_tS))

barplot(accuracy_tS, names.arg=c('Eng', 'Jap'), main='Accuracy of tʃ-production', ylim=c(0,0.6))


S = data_frame(Language=factor(c('English', 'Japanese'), levels=c('English', 'Japanese')),Accuracy=accuracy_tS)


ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of tʃ-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14))+
  xlab('')


###########################################################
# /ts/

Grk_ts = c(rep.int(1,101), rep.int(0,250))
Chi_ts = c(rep.int(1,161), rep.int(0,292))
Jap_ts = c(rep.int(1,33), rep.int(0,82))

wilcox.test(Grk_ts, Chi_ts)
wilcox.test(Grk_ts, Jap_ts)
wilcox.test(Jap_ts, Chi_ts)

prop.test(c(sum(Grk_ts), sum(Chi_ts)), c(length(Grk_ts), length(Chi_ts)), correct=FALSE)
prop.test(c(sum(Grk_ts), sum(Jap_ts)), c(length(Grk_ts), length(Jap_ts)), correct=FALSE)
prop.test(c(sum(Jap_ts), sum(Chi_ts)), c(length(Jap_ts), length(Chi_ts)), correct=FALSE)


accuracy_ts = c(sum(Grk_ts)/length(Grk_ts), sum(Chi_ts)/length(Chi_ts), sum(Jap_ts)/length(Jap_ts))

barplot(accuracy_s, names.arg=c('Grk', 'Can', 'Jap'), main='Accuracy of ts-production', ylim=c(0,0.6))

S = data_frame(Language=factor(c('Greek', 'Cantonese', 'Japanese'), levels=c('Greek', 'Cantonese', 'Japanese')),Accuracy=accuracy_ts)

ggplot(data=S, aes(x=Language, y=Accuracy)) +
  geom_bar(stat='identity', fill='red') +
  ggtitle('Accuracy of ts-production') +
  theme_classic() +
  theme(plot.title = element_text(hjust=0.5), text=element_text(size=14))+
  geom_signif(comparisons = list(c("Cantonese", "Greek")), annotations = '*', size=1, margin_top=0.3, tip_length=0.2) +
  xlab('')

