library(types)
library(here)

load_dist_mtx <- function(input_filename = ? character) {
  dist_mtx <- read.csv(input_filename, header = T, sep = ";")
  rownames(dist_mtx) <- dist_mtx[, 1]
  return(dist_mtx[, 2:length(dist_mtx)])
}

heatmap <- function(dm = ? data.frame, show_values = TRUE) {
  # credit: https://stackoverflow.com/a/3082602
  dst <- data.matrix(dm)
  dim <- ncol(dst)
  image(1:dim, 1:dim, dst, axes = FALSE, xlab = "", ylab = "")
  if (show_values) {
    text(expand.grid(1:dim, 1:dim), sprintf("%0.1f", dst), cex = 0.6)
  }
}

dm <- load_dist_mtx(here("data/out/test_pipeline/dm.csv"))
system.time(heatmap(as.matrix(dm)))

dm <- load_dist_mtx(here("data/out/real_data/snp_matrix_significant.csv"))
system.time(heatmap(as.matrix(dm), FALSE)) # Alas! Runs ~3 min, result - a black rectangle
