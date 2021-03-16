library(tidyverse)
library(lme4)
library(ggsignif)

#####################################
#4.3.4 Results - Linear regression
#####################################

eng <- read_tsv('eng-regression.txt') 
chi <- read_tsv('chi-regression.txt') 
grk <- read_tsv('grk-regression.txt') 
jap <- read_tsv('jap-regression.txt') 

eng_tidy <- eng %>%
  mutate(lang = 'eng')

chi_tidy <- chi %>%
  mutate(lang = 'chi')

grk_tidy <- grk %>%
  mutate(lang = 'grk')

jap_tidy <-jap %>%
  mutate(lang = 'jap')


data <-  eng_tidy %>%
  full_join(grk_tidy) %>%
  full_join(chi_tidy) %>%
  full_join(jap_tidy)

predictors <- data %>%
  select(freqToken, freqType, flToken, flType)

cor(predictors)

##########################################################
#1. English

lang = eng_tidy

m1 = lm(accuracy ~ flType + complexity, data=lang)
summary(m2)

m2 = lm(accuracy ~ flToken + complexity, data=lang)
summary(m2)

m3 = lm(accuracy ~ freqType + complexity, data=lang)
summary(m3)

m4 = lm(accuracy ~ freqToken + complexity, data=lang)
summary(m4)


##########################################################
#2. Cantonese

lang = chi_tidy

m1 = lm(accuracy ~ flType + complexity, data=lang)
summary(m1)

m2 = lm(accuracy ~ flToken + complexity, data=lang)
summary(m2)

m3 = lm(accuracy ~ freqType + complexity, data=lang)
summary(m3)

m4 = lm(accuracy ~ freqToken + complexity, data=lang)
summary(m4)

##########################################################
#3. Greek

lang = grk_tidy

m1 = lm(accuracy ~ flType + complexity, data=lang)
summary(m1)

m2 = lm(accuracy ~ flToken + complexity, data=lang)
summary(m2)

m3 = lm(accuracy ~ freqType + complexity, data=lang)
summary(m3)

m4 = lm(accuracy ~ freqToken + complexity, data=lang)
summary(m4)

##########################################################
#4. Japanese

lang = jap_tidy

m1 = lm(accuracy ~ flType + complexity, data=lang)
summary(m1)

m2 = lm(accuracy ~ flToken + complexity, data=lang)
summary(m2)

m3 = lm(accuracy ~ freqType + complexity, data=lang)
summary(m3)

m4 = lm(accuracy ~ freqToken + complexity, data=lang)
summary(m4)