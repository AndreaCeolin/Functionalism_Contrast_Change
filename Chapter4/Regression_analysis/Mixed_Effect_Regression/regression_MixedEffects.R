library(tidyverse)
library(lme4)


############################################
#4.3.5 Results - Mixed Effect Logistic Regression
############################################



############################################
#1. Measures


eng_measures <- read_tsv('eng-regression.txt') 
chi_measures <- read_tsv('chi-regression.txt') 
grk_measures <- read_tsv('grk-regression.txt') 
jap_measures <- read_tsv('jap-regression.txt') 

eng_measures_tidy <- eng_measures %>%
  mutate(lang = 'English', freqToken = scale(freqToken), freqType = scale(freqType), flToken=scale(flToken), flType=scale(flType))

chi_measures_tidy <- chi_measures %>%
  mutate(lang = 'Chinese', freqToken = scale(freqToken), freqType = scale(freqType), flToken=scale(flToken), flType=scale(flType))

grk_measures_tidy <- grk_measures %>%
  mutate(lang = 'Greek', freqToken = scale(freqToken), freqType = scale(freqType), flToken=scale(flToken), flType=scale(flType))

jap_measures_tidy <-jap_measures %>%
  mutate(lang = 'Japanese', freqToken = scale(freqToken), freqType = scale(freqType), flToken=scale(flToken), flType=scale(flType))

data_measures <-  eng_measures_tidy %>%
  full_join(grk_measures_tidy) %>%
  full_join(chi_measures_tidy) %>%
  full_join(jap_measures_tidy)

data_measures <- data_measures %>%
  rename(target=consonant)

############################################
#2. Data

eng <- read_tsv('up-eng.txt') 
chi <- read_tsv('up-chi.txt') 
grk <- read_tsv('up-grk.txt') 
jap <- read_tsv('up-jpn.txt') 

data <-  eng %>%
  full_join(grk) %>%
  full_join(chi) %>%
  full_join(jap)

data_tidy <- data_measures %>%
  inner_join(data, by='target') %>%
  filter(correct!='m') 


############
#3. Analysis

m1 = glmer(as.numeric(correct) ~ flType + (1|complexity) + (1|lang.x) + (1|age) + (1|word) + (1|child), family=binomial, data=data_tidy)
summary(m1)

m2 = glmer(as.numeric(correct) ~ flToken + (1|complexity)  + (1|lang.x) + (1|age) + (1|word) + (1|child), family=binomial, data=data_tidy)
summary(m2)

m3 = glmer(as.numeric(correct) ~ freqType + (1|complexity) + (1|lang.x) + (1|age) + (1|word) + (1|child), family=binomial, data=data_tidy)
summary(m3)

m4 = glmer(as.numeric(correct) ~ freqToken + (1|complexity)  + (1|lang.x) + (1|age) + (1|word) + (1|child), family=binomial, data=data_tidy)
summary(m4)

##############
#4. Case studies

thinking <- data %>%
  filter(word=="thinking")

thinking_1 <- thinking %>%
  filter(correct==1)

thinking_0 <- thinking %>%
  filter(correct==0)

thin <- data %>%
  filter(word=="thin")

thin_1 <- thin %>%
  filter(correct==1)

thin_0 <- thin %>%
  filter(correct==0)

thio <- data %>%
  filter(word=="thio")

thio_1 <- thio %>%
  filter(correct==1)

thio_0 <- thio %>%
  filter(correct==0)
