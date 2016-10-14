// view for nsx_edge docs
// returns loadbalancer sub-jsons

function(doc) {
    
    var key ; 
    var loadbalancer ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_edge") != -1
            && doc.featureConfigs.features
            && doc.id
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = doc.id ;
        features = doc.featureConfigs.features ;
        

        // loop the features & find the correct one
        features.forEach(function(feature) {
            if (feature.featureType == "loadbalancer_4.0") {
                loadbalancer = feature ;
                // map only when found    
                key = [collect, client, source, id]  ;
                emit( key,  {"loadbalancer":loadbalancer} );
            }
        }) ;

    }
}