stat_bin_hex <- function(mapping = NULL, data = NULL, geom = "hex",
                         position = "identity", bins = 30, 
                         binwidth = NULL, na.rm = FALSE, 
                         show.legend = NA, inherit.aes = TRUE, ...) {
    layer(
          data = data,
          mapping = mapping,
          stat = StatBinhex,
          geom = geom,
          position = position,
          show.legend = show.legend,
          inherit.aes = inherit.aes
          params = list(
            bins = bins,
            binwidth = binwidth,
            na.rm = na.rm,
            ...
            )
          )
}

stat_binhex <- stat_bin_hex

StatBinhex <- ggproto("StatBinhex", Stat, 
    default_aes = aes(fill = ..count..),
    required_aes = c("x", "y"),
    compute_group = function(data, scales, binwidth = NULL, bins = 30,
                             na.rm = FALSE) {
        if (is.null(binwidth)) {
            binwidth <- c(diff(scales$x$dimension()) / bins,
                          diff(scales$y$dimension()) / bins
                          )
        }
        hexBin(data$x, data$y, binwidth)
    }
)

hexBin <- function(x, y, binwidth) {
    xbnds <- c(plyr::round_any(min(x), binwidth[1], floor) - 1e-6,
               plyr::round_any(max(x), binwidth[1], ceiling) + 1e-6
               )
    xbins <- diff(xbnds) / binwidth[1]
    ybnds <- c(plyr::round_any(min(x), binwidth[2], floor) - 1e-6,
               plyr::round_any(max(x), binwidth[2], ceiling) + 1e-6
               )
    ybins <- diff(ybnds) / binwidth[2]

    hb <- hexbin::hexbin(
                         x, xbnds = xbnds, xbins = xbins,
                         y, ybnds = ybnds, shape = ybins/xbins
    )

    data.frame(
               hexbin::hcell2xy(hb),
               count = hb@count,
               density = hb@count / sum(hb@count, na.rm = TRUE)
               )
}

