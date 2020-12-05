library(uwot)
library(cowplot)

training <- read.table("training.txt")
dim(training)
training <- training[, 6:ncol(training)]

new_train <- training[,seq(1, ncol(training), 2)] + training[,seq(2, ncol(training), 2)]

##################################################################

scale_expr_umap <- uwot::umap(t(new_train), pca = 200)

library(ggplot2)
library(viridis)
plot_df <- data.frame(scale_expr_umap)
colnames(plot_df) <- c("umap1", "umap2")
ggplot(plot_df, aes(umap1, umap2)) + geom_point(size = 3) +
  theme_cowplot(16)

library(Rtsne)
tsne_plot <- Rtsne(t(new_train),dims=2, perplexity=50, check_duplicates = FALSE)
tsne_df <- data.frame(tsne_plot$Y)
colnames(tsne_df) <- c("tSNE1", "tSNE2")


ggplot(tsne_df, aes(tSNE1, tSNE2)) + geom_point(size=3) + theme_cowplot(16)





