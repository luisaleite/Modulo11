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
library(corrplot)
library(factoextra)


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


#Analise univariada

table(employee$store_id)
table(employee$role)
table(employee$status)

table(store$store_id)

table(transations$cod_loja)

# Filtrar as linhas que contêm 'SP Interior_93' na coluna store_id
transations_filtered <- subset(transations, cod_loja %in% c("MG_24", "MG_29"))

# Exibir as primeiras linhas do dataset filtrado
head(transations_filtered)

table(transations_filtered$cod_loja)
table(transations_filtered$quantidade)

# Histogramas
hist(transations_filtered$quantidade)

# Gráficos de densidade
plot(density(transations_filtered$quantidade))

# Boxplots
boxplot(transations_filtered$quantidade)

library(dplyr)

soma_quantidade <- transations %>%
  group_by(cod_loja) %>%
  summarise(soma_quantidade = sum(quantidade))

# Histogramas
hist(store$sales_target)

# Gráficos de densidade
plot(density(store$sales_target))

# Boxplots
boxplot(store$sales_target)

# Identificação de outliers
boxplot(transations$quantidade)$out

# Carregar pacotes necessários
library(ggplot2)

# Carregar os dados
data <- read.csv("C:/Users/Inteli/Downloads/transaction_fact_v3_2024.csv")

# Histograma para a variável 'quantidade'
ggplot(data, aes(x = quantidade)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black", alpha = 0.7) +
  labs(title = "Histograma de Quantidade", x = "Quantidade", y = "Frequência")

# Histograma para a variável 'preco'
ggplot(data, aes(x = preco)) +
  geom_histogram(binwidth = 10, fill = "green", color = "black", alpha = 0.7) +
  labs(title = "Histograma de Preço", x = "Preço", y = "Frequência")

# Gráfico de densidade para a variável 'quantidade'
ggplot(data, aes(x = quantidade)) +
  geom_density(fill = "blue", alpha = 0.5) +
  labs(title = "Gráfico de Densidade de Quantidade", x = "Quantidade", y = "Densidade")

# Gráfico de densidade para a variável 'preco'
ggplot(data, aes(x = preco)) +
  geom_density(fill = "green", alpha = 0.5) +
  labs(title = "Gráfico de Densidade de Preço", x = "Preço", y = "Densidade")

# Boxplot para a variável 'quantidade'
ggplot(data, aes(y = quantidade)) +
  geom_boxplot(fill = "blue", alpha = 0.7) +
  labs(title = "Boxplot de Quantidade", y = "Quantidade")

# Boxplot para a variável 'preco'
ggplot(data, aes(y = preco)) +
  geom_boxplot(fill = "green", alpha = 0.7) +
  labs(title = "Boxplot de Preço", y = "Preço")

# Identificar outliers na variável 'quantidade'
quantidade_outliers <- boxplot.stats(data$quantidade)$out
print("Outliers em 'quantidade':")
print(quantidade_outliers)

# Identificar outliers na variável 'preco'
preco_outliers <- boxplot.stats(data$preco)$out
print("Outliers em 'preco':")
print(preco_outliers)



# Carregar pacotes necessários
library(ggplot2)
library(corrplot)

# Gráfico de dispersão entre 'quantidade' e 'preco'
ggplot(transations, aes(x = quantidade, y = preco)) +
  geom_point(color = "blue", alpha = 0.6) +
  labs(title = "Relação entre Quantidade e Preço", x = "Quantidade", y = "Preço")

# Gráfico de barras para explorar a relação entre 'cod_loja' e 'quantidade'
ggplot(transations, aes(x = cod_loja, y = quantidade)) +
  geom_bar(stat = "identity", fill = "orange") +
  labs(title = "Quantidade Vendida por Loja", x = "Código da Loja", y = "Quantidade") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Gráfico de barras para explorar a relação entre 'cod_loja' e 'preco'
ggplot(transations, aes(x = cod_loja, y = preco)) +
  geom_bar(stat = "identity", fill = "green") +
  labs(title = "Preço Médio por Loja", x = "Código da Loja", y = "Preço") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Cálculo da matriz de correlação entre as variáveis numéricas
correlacao <- cor(transations[, c("quantidade", "preco")], use = "complete.obs")

# Visualização da matriz de correlação
corrplot(correlacao, method = "circle", type = "upper", 
         tl.col = "black", tl.srt = 45)




# Instalar e carregar pacotes necessários
install.packages("FactoMineR")  # Caso ainda não tenha o pacote instalado
install.packages("factoextra")  # Para visualização dos resultados
library(FactoMineR)
library(factoextra)

# Carregar os dados
data <- read.csv("C:/Users/Inteli/Downloads/transaction_fact_v3_2024.csv")

# Selecionar as variáveis numéricas para o PCA
data_numeric <- data[, c("quantidade", "preco")]

# Realizar a Análise de Componentes Principais (PCA)
pca_result <- prcomp(data_numeric, scale. = TRUE)

# Resumo dos resultados do PCA
summary(pca_result)

# Visualizar a variância explicada pelos componentes principais
fviz_eig(pca_result, addlabels = TRUE, ylim = c(0, 100))

# Visualizar as variáveis nos componentes principais
fviz_pca_var(pca_result, col.var = "cos2",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE)

# Visualizar as observações nos componentes principais
fviz_pca_ind(pca_result, geom.ind = "point", pointshape = 21,
             pointsize = 2, fill.ind = data$cod_loja,
             col.ind = "black", palette = "jco",
             addEllipses = TRUE, ellipse.level = 0.95,
             repel = TRUE)
