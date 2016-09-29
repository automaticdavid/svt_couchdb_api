// function(doc) {
//     var monitor, id, name ;
//     if (doc.edge && doc.monitor) {
//         for (monitor in doc.monitor) {
//             name = monitor["name"]["$"];
//             id = monitor["monitorId"]["$"];
//             emit(name, id);
//         }
//     }
// }



// function(doc) {
//     var key ; 
//     if (doc.edge.id && doc.edge.features.loadBalancer && doc.edge.vnics) {
// 	    key = doc.edge.id.$ ;
//             emit( key, {"vnics" : doc.edge.vnics, "loadbalancer": doc.edge.features.loadBalancer} );
//         }
//     }



// function(doc) {
//     var key ; 
//     if (doc.ehc_collect_date 
//         && doc.edge.id 
//         && doc.edge.features.loadBalancer 
//         && doc.edge.vnics) {
                
//         key = [doc.ehc_collect_date, doc.edge.id.$] ;
//         emit( key, {"vnics" : doc.edge.vnics, 
//                     "loadbalancer": doc.edge.features.loadBalancer} );
//         }
//     }


// function(doc) {
//     var key ; 
//     if (doc.ehc_collect_date 
//             && doc.ehc_source_dir
//             && doc.edge.id 
//             && doc.edge.features.loadBalancer 
//             && doc.edge.vnics
//             && doc.edge.vnics.vnic) {
                
//         key = [doc.ehc_collect_date, doc.ehc_source_dir, doc.edge.id.$]  ;
//         emit( key, {"vnics" : doc.edge.vnics.vnic, 
//                     "loadbalancer": doc.edge.features.loadBalancer} );
//         }
//     }


// function(doc) {
//     var key ; 
//     if (doc.ehc_collect_date 
//             && doc.ehc_source_dir
//             && doc.edge.id 
//             && doc.edge.features.loadBalancer 
//             && doc.edge.vnics
//             && doc.edge.vnics.vnic) {
        
//         // name the docs and
//         collect = doc.ehc_collect_date ; 
//         source = doc.ehc_source_dir ;
//         loadBalancer = doc.edge.features.loadBalancer ; 
//         vnics = doc.edge.vnics.vnic ;
//         edgeId = doc.edge.id.$ ;
        
//         //deal with the vnics list of dict
//         var n_vnics = [] ;
//         vnics.forEach(function(d) {
//             var v = {} ;
//             v.svt_unic = d.label.$ ;
//             v.svt_value = d ;
//             n_vnics.push(v) ;
//         });
        
//         // map    
//         key = [collect, source, edgeId]  ;
//         emit( key, {"vnics" : n_vnics, 
//                     "loadbalancer": loadBalancer} );
//         }
//     }



function(doc) {
    
    var key ; 
    var loadbalancer ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("edge") != -1
            && doc.featureConfigs.features
            && doc.id
        
        ) {
        
        // name the docs
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


function(doc) {
    
    var key ; 
    var volumes ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("block-volumes") != -1
            && doc.name
        
        ) {
        
        // name the docs
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = doc.name ;
        
        // loop the doc and follow links
        // doc.forEach(function(it) {
            

        // }) ;


        // map all volumes   
        key = [collect, client, source, id]  ;
        emit( key,  {"volumes":doc} );
        
    }
}

    
    var key ; 
    var links = {} ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_") != -1
            && doc.id
        
        ) {
        
        // name the docs
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        svt_urn = doc.id ;
        
        // map with the urn as key for values
        links[svt_urn] = doc ;
        key = [collect, client, source]  ;
        emit( key,  links );
        
    }
}