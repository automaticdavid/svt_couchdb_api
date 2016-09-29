// view for nsx_edge docs
// returns vnics sub-jsons
// normalizes result with a unique key 


function(doc) {
    
    var key ; 
    var normalized_vnics = [] ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("edge") != -1
            && doc.vnics.vnics
            && doc.id
        
        ) {
        
        // name the docs
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = doc.id ;
        vnics = doc.vnics.vnics ;
        
        // loop the features & find the correct one
        vnics.forEach(function(vnic) {
            var v = {} ;
            v.svt_unic = vnic.label ;
            v.svt_value = vnic ;
            normalized_vnics.push(v) ; 
        }) ;

        // map all vnics   
        key = [collect, client, source, id]  ;
        emit( key,  {"vnics":normalized_vnics} );
        
    }
}