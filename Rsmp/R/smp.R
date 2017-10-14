#' @importFrom dplyr %>% if_else
#' @importFrom rlang .data quo enquo quo_name
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
                          json_key_suffix = "",
                          select_keys_to_populate = TRUE) {
  quosures <- keys_to_populate %>%
    purrr::map_chr(~glue("{json_field} ->> '{.}'")) %>%
    purrr::map(~quo(sql(!!.))) %>%
    purrr::set_names(paste0(json_key_suffix, keys_to_populate))

  result <- dplyr::mutate(.data, !!!quosures)

  if (select_keys_to_populate) {
    result <- dplyr::select(result, !!keys_to_populate)
  }

  result
}

#' Scrapy Scrape Table
#'
#' @export
data_scrape <- function(keys_to_populate, callback_function = NULL,
                        use_last_spider_results = TRUE,
                        select_populated = TRUE) {
  scraped_item <- dplyr::tbl(db_con(), "mvp_scrapeditem")

  if (!is.null(callback_function)) {
    scraped_item <- dplyr::filter(scraped_item,
                                  callback_function == !!callback_function)
  }

  if (use_last_spider_results) {
    scraped_item <- filter_last_spider_run(scraped_item)
  }

  populated <- json_populate(scraped_item, "item", keys_to_populate)

  if (select_populated) {
    dplyr::select(populated, !!keys_to_populate)
  }
}

#' Softonic Apps
#'
#' @export
data_softonic_app <- function(use_last_spider_results = TRUE) {
  scraped_item <- dplyr::tbl(db_con(), "mvp_scrapeditem")

  if (use_last_spider_results) {
    scraped_item <- filter_last_spider_run(scraped_item)
  }

  apps <- scraped_item %>%
    dplyr::filter(callback_function == "parse_app_list") %>%
    json_populate(
      "item",
      c("url", "cons", "name", "pros", "type", "score", "votes", "license",
        "summary", "version", "category", "language", "logo_url", "platform",
        "page_order", "page_number", "sub_category", "download_count"))

  apps %>%
    dplyr::mutate(score = if_else(score == "-", NA, score)) %>%
    dplyr::mutate(download_count_prefix = sql("substring(download_count, '[^0-9]+')")) %>%
    dplyr::mutate(download_count = as.integer(sql("substring(download_count, '[0-9]+')"))) %>%
    dplyr::mutate(download_count = if_else(download_count_prefix == "M", download_count * (10 ** 6),
                                           if_else(download_count_prefix == "K", download_count * (10 ** 3),
                                                   download_count))) %>%
    dplyr::select(-.data$download_count_prefix) %>%
    dplyr::mutate(votes = as.integer(votes))
}

filter_last_spider_run <- function(.data) {
  last_spider_run <- dplyr::tbl(db_con(), "mvp_scrapeditem") %>%
    dplyr::summarise(spider_load_time = max(spider_load_time))

  dplyr::semi_join(.data, last_spider_run, by = "spider_load_time")
}

#' Arrange Descending Nulls Last
#'
#' PostgreSQL helper function
#'
#' @export
desc_nulls_last <- function(.data, column) {
  sql_stmt <- glue("{column} DESC NULLS LAST")
  dplyr::arrange(.data, sql(sql_stmt))
}
