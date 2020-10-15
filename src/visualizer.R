library(types)

load_dist_mtx = function(input_filename = ? character) {
  read.table(input_filename)
}

heatmap = function(dm = ? data.frame){
  # credit: https://stackoverflow.com/a/3082602
  dst <- data.matrix(dm)
  dim <- ncol(dst)
  image(1:dim, 1:dim, dst, axes = FALSE, xlab="", ylab="")
  text(expand.grid(1:dim, 1:dim), sprintf("%0.1f", dst), cex=0.6)
}

force_directed_graph = function(dm = ? data.frame, out_filename = ? character){
  dist_m <- as.matrix(dm)
  dist_mi <- 1/dist_m # one over, as qgraph takes similarity matrices as input
  library(qgraph)
  jpeg(out_filename, width=1000, height=1000, unit='px')
  qgraph(dist_mi, layout='spring', vsize=3)
  dev.off()
}

dm <- load_dist_mtx("../data/out/test/snp_matrix.txt")
system.time(heatmap(dm))
system.time(force_directed_graph(dm, "../data/out/vis/test_force_graph.jpg"))
