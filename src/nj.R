# Title     : Neighborhood joining tree
# Objective : NJ tree for distance matrices calculated in Python code
# Created by: Valera
# Created on: 11/11/2020

library(ape)
library(here)

data_dir <- here("data/out/real_data/")
abs_path <- function(rel_path = ?str) {
  paste0(data_dir, rel_path)
}
lapply(list(
  list(dm_path = "/snp_matrix_significant.csv", out_path = "/nj_tree_significant.png", comment = "filtered SNPs"),
  list(dm_path = "/snp_matrix.csv", out_path = "/nj_tree_not_filtered.png", comment = "all SNPs")
), function(params) {
  dm <- read.csv(abs_path(params$dm_path), sep = ";")
  png(filename = abs_path(params$out_path))
  plot(nj(as.matrix(dm)[, -1]), main = paste("Neighborhood joining tree for distance matrix :", params$comment))
  dev.off()

})
