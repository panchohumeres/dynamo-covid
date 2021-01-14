function total() {
  
    var paises = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('countries').getDataRange().getValues();
    var urls= [];
    var status=[];
      
      paises.forEach(function(elem,i){
    
      
      urls.push(elem[3])
      
       });
  
    urls=urls.slice(1)
  
    function fetchURL (url){
    
     Logger.log(url);
  
    var response = UrlFetchApp.fetch(url, {
              "method": "get",
              'contentType': 'application/json'
    
              });
    
  
  
    try {
     
     var json = response.getContentText();
    var data = JSON.parse(json);
    var headers = Object.keys(data[0]);
    var output = [];
    output.push(headers);
    
    
    
    data.forEach(function(elem,i){
    
      var vals = Object.values(elem)
      output.push(vals) });
  
   // Logger.log(Object.values(output));
    
    
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('data').getDataRange().getValues();
    
      var nrows = output.length;
    var ncols = headers.length;
    
      //range and last row with data
    var actual_data_range = sheet.getDataRange();
  var last_row = actual_data_range.getLastRow();
  var last_column = actual_data_range.getLastColumn();
    
    sheet.getRange(last_row,1,nrows,ncols).setValues(output)
    ok.push(url)
  ok.push('OK')
  status.push(ok)
    
    }
  
    catch (err){ 
  
  var ok=[]
  ok.push(url)
  ok.push(err)
  status.push(ok)
  
  
    }
  
  
    }
    
   var processed=[]
  
  
    urls.forEach(function(elem,i){
    
    fetchURL(elem)
    processed.push(elem)
    
     });
  
  Logger.log(processed);
  
  }
  