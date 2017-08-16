// view for nsx_edge docs
// returns bgpNeighbours sub-jsons

function(doc) {
    
    var key ; 
    var normalized_bgpNeighbours  = [] ;

    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_edge") != -1
            && doc.featureConfigs
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
            
            if (feature.featureType == "routing_4.0") {
                
                bgp = feature ;
                
                if (bgp.bgp
                    && bgp.bgp.bgpNeighbours
                    && bgp.bgp.bgpNeighbours.bgpNeighbours
                    ) {

                    bgpNeighbours = bgp.bgp.bgpNeighbours.bgpNeighbours ;
                    
                    bgpNeighbours.forEach(function(bgpNeighbour) {
                        if (bgpNeighbour.ipAddress) {
                            var v = {} ;
                            v.svt_unic = bgpNeighbour.ipAddress ;
                            v.svt_value = bgpNeighbour ;
                            normalized_bgpNeighbours.push(v) ;
                        } 
                    }) ;
                
                }
            }
        
        // map only when found    
        key = [collect, client, source, id]  ;
        emit( key,  {"bgpNeighbours":normalized_bgpNeighbours, 'svt_action':'svt_standard'} );
        
        }) ;

    }
}
