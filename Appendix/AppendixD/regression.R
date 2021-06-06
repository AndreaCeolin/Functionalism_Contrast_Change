# author: Andrea Ceolin
# date: December 2020


library(tidyverse)
library(lme4)

#Load the data with tidyverse
data = read_tsv('fl_data.tsv') %>% 
  mutate(max_freq=pmax(Freq1,Freq2)) %>%
  mutate(nomp=ifelse(MinPairs==0, 0, 1)) %>% 
  group_by(Type) %>%
  mutate(freq=scale(max_freq)) %>%
  mutate(entropy=scale(EntropyLoss))


#Model with Minimal Pairs and Frequency as predictors
mD2 = glmer(Merged ~ log(MinPairs+1) + freq*nomp + (1|Type), family=binomial, data=data)
summary(mD2)

#Model with Entropy and Frequency as predictors
mD3 = glmer(Merged ~ entropy + freq*nomp + (1|Type), family=binomial, data=data)
summary(mD3)


#Create two separate datasets for conditioned and unconditioned mergers 
unconditioned = data %>%
  filter(Environment == 'Unconditioned')
  
conditioned = data %>%
  filter(Environment == 'Conditioned')



#Model with Minimal Pairs and Frequency as predictors of unconditioned mergers 
mD4 = glmer(Merged ~ log(MinPairs+1) + freq + nomp + (1|Type), family=binomial, data=unconditioned)
summary(mD4)

#Model with Minimal Pairs and Frequency as predictors of conditioned mergers
mD5 = glmer(Merged ~ log(MinPairs+1) + freq + nomp + (1|Type), family=binomial, data=conditioned)
summary(mD5)

