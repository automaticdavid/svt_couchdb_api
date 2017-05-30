// view for vipr docs
// returns vdc-network-systems sub-jsons


function(doc) {

    var key ;
    

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_vdc-network-systems_") != -1
            
        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ; 
        filename = file.split("_")[2] ;
        id = filename.split(".")[0] ;
        

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"network-systems":doc, "svt_action":"svt_multi"} );

    }
}