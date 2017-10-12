#' @importFrom dplyr %>%
#' @importFrom dplyr if_else
#' @importFrom rlang .data quo
#' @importFrom assertthat assert_that
#' @importFrom glue glue
NULL

#' Database Connection
#'
#' @export
db_con <- memoise::memoise(function() {
  DBI::dbConnect(
    RPostgreSQL::PostgreSQL(),
    user = Sys.getenv("SMP_DB_USER"),
    password = Sys.getenv("SMP_DB_PASSWORD"),
    host = Sys.getenv("SMP_DB_HOST"),
    port = as.integer(Sys.getenv("SMP_DB_PORT")),
    dbname = Sys.getenv("SMP_DB_NAME")
  )
})

#' PostgreSQL Json Populate
#'
#' @export
json_populate <- function(.data, json_field, keys_to_populate,
                          json_key_suffix = "", unselect_json_field = TRUE) {
  quosures <- keys_to_populate %>%
    purrr::map_chr(~glue("{json_field} ->> '{.}'")) %>%
    purrr::map(~quo(sql(!!.))) %>%
    purrr::set_names(paste0(json_key_suffix, keys_to_populate))

  dplyr::mutate(.data, !!!quosures) %>%
    dplyr::select(-.data[[json_field]])
}

#' Scrapy Scrape Table
#'
#' @export
data_scrapy_scrape <- function(keys_to_populate, callback_function = NULL) {
  scraped_item <- dplyr::tbl(db_con(), "mvp_scrapeditem")

  if (!is.null(callback_function)) {
    scraped_item <- dplyr::filter(scraped_item,
                                  callback_function == !!callback_function)
  }

  json_populate(scraped_item, "item", keys_to_populate)
}
