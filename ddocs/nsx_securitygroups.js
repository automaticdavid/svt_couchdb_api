// view for nsx_securitygroups docs
// returns all securitygroups sub-jsons


function(doc) {
    
    var key ; 
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_securitygroup") != -1
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ; 
        filename = file.split("_")[2] ;
        name = filename.split(".")[0] ; 

        // map all vnics   
        key = [collect, client, source, name ]  ;
        emit( key, {"securitygroups" : doc, "svt_action":"svt_multi" } );
        
    }
}