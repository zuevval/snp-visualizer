library(types)

load_dist_mtx = function(input_filename = ? character) {
  read.table(input_filename)
}

heatmap = function(dm = ? data.frame, show_values = TRUE){
  # credit: https://stackoverflow.com/a/3082602
  dst <- data.matrix(dm)
  dim <- ncol(dst)
  image(1:dim, 1:dim, dst, axes = FALSE, xlab="", ylab="")
  if(show_values){
    text(expand.grid(1:dim, 1:dim), sprintf("%0.1f", dst), cex=0.6)
  }
}

force_directed_graph = function(dm = ? data.frame, out_filename = ? character){
  dist_m <- as.matrix(dm)
  dist_mi <- 1/dist_m # one over, as qgraph takes similarity matrices as input
  library(qgraph)
  jpeg(out_filename, width=1000, height=1000, unit='px')
  qgraph(dist_mi, layout='spring', vsize=3)
  dev.off()
}

measure_time <- function(n = ? numeric){
  input_filename = paste("../data/out/real_data/snp_matrix_", as.character(n), ".txt", sep="")
  out_graph_filename = paste("../data/out/vis/real_data/force_graph_", as.character(n), ".jpg", sep="")
  dm <- load_dist_mtx(input_filename)
  heatmap(dm)
  system.time(force_directed_graph(dm, out_graph_filename))
}

lapply(c(10, 20, 30, 40, 50), measure_time)
  

dm <- load_dist_mtx("../data/out/test/snp_matrix.txt")
system.time(heatmap(dm))
system.time(force_directed_graph(dm, "../data/out/vis/test_force_graph.jpg"))

setwd("E:/Users/vzuev/github-zuevval/snp-visualizer/src")
dm <- load_dist_mtx("../data/out/real_data/snp_matrix.txt")
system.time(force_directed_graph(dm, "../data/out/vis/real_data/force_graph.jpg"))
system.time(heatmap(dm), FALSE)
