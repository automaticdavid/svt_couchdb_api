
function(doc) {
    
    var key ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_compute-cluster") != -1
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ; 
        filename = file.split("_")[2] ;
        id = filename.split(".")[0] ; 

        key = [collect, client, source, id ]  ;

        if (file.indexOf("vipr_compute-cluster-host")) {
            emit( key, {"clusters-combine" : {"cluster":doc} , "svt_action":"svt_multi" } );
        } else {
            emit( key, {"clusters-combine" : doc, "svt_action":"svt_multi" } );
        }
        
    }
}
