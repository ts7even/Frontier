use yahoo_finance_api as yahoo;
//use std::time::{Duration, UNIX_EPOCH};
//use chrono::{Utc,TimeZone};
// use tokio_test;

mod nasdaq;
fn main() {
    let ticker = nasdaq::tickers;
    let provider = yahoo::YahooConnector::new();
    for t in ticker {
        let response = provider.get_quote_range(t, "1d", "5y").unwrap();
        let quotes = response.quotes().unwrap();
        println!("{}", t);
        for item in quotes
        {
            let adj = item.adjclose;
            println!("{:.2}", adj)    
    }
  }
}