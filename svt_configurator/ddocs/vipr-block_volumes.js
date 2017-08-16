// view for vipr_block docs
// returns block-volume sub-jsons

function(doc) {
    
    var key ; 
    var volumes ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_block-volumes") != -1
            && doc.name
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = doc.name ;
        
        // map all volumes   
        key = [collect, client, source, id]  ;
        emit( key,  {"volumes":doc} );
        
    }
}