function countries() {
  

    url='https://api.covid19api.com/countries'
    
    
    var response = UrlFetchApp.fetch(url, {
              "method": "get",
              'contentType': 'application/json'
    
              });
    
    
     var json = response.getContentText();
    var data = JSON.parse(json);
    var headers = Object.keys(data[0]);
    headers.push('URL_TOTAL')
    var output = [];
    var urls=[];
    output.push(headers);
    
    url='https://api.covid19api.com/total/dayone/country/'
    
    data.forEach(function(elem,i){
    
      var vals = Object.values(elem)
      vals.push(url+vals[1])
      output.push(vals)
      
       });
  
    Logger.log(Object.values(output));
    
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('countries');
    
      var nrows = output.length;
    var ncols = headers.length;
    
      //range and last row with data
    var actual_data_range = sheet.getDataRange();
    
    sheet.getRange(1,1,nrows,ncols).setValues(output)
  
  
  
  
  
  
  
  }
  