# Instalar pacotes necessários
install.packages(c("tidyverse", "data.table", "GGally", "corrplot", "gridExtra"))
install.packages("rmarkdown")


# Carregar pacotes
library(tidyverse)
library(data.table)
library(GGally)
library(corrplot)
library(gridExtra)
library(dplyr)

# Lendo as bases
status <- read.csv("C:/Users/Inteli/Downloads/sku_status_dataset_updated.csv")
cost <- read.csv("C:/Users/Inteli/Downloads/sku_cost (1).csv") 
price <- read.csv("C:/Users/Inteli/Downloads/sku_price (1).csv") 
employee <- read.csv("C:/Users/Inteli/Downloads/employee_final (1).csv")
store <- read.csv("C:/Users/Inteli/Downloads/target_store_final_v3 (1).csv")
transations <- read.csv("C:/Users/Inteli/Downloads/transaction_fact_v3_2024.csv")

# Mostrando as primeiras linhas das tabelas
status %>% slice(1:6)
cost %>% slice(1:6)
price %>% slice(1:6)
employee %>% slice(1:6)
store %>% slice(1:6)
transations %>% slice(1:6)

#Mostrando a estrutura dos dados de cada tabela
str(status)
str(cost)
str(price)
str(employee)
str(store)
str(transations)

# Aqui consegui um resumo estatistico de cada tabela
summary(status)
summary(cost)
summary(price)
summary(employee)
summary(store)
summary(transations)





