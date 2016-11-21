// view for nsx_appliance docs
// returns all management sub-jsons


function(doc) {
    
    var key ;
    var val = {} ; 
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_appliance-management") != -1
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ; 
        elems = file.split("-").slice(2) ;
        infos = elems.join("-") ; 
        id = infos.split(".")[0] ; 
        
        // Rekey & map for components
        if (doc.components
        && doc.svt_source_file.indexOf("nsx_appliance-management-components.json") != -1
        ) {
            var normalized_components = [] ;
            components = doc.components ;
            components.forEach(function(component) {
                var v = {} ;
                if (component.componentId) {
                    v.svt_unic = component.componentId ;
                    v.svt_value = component ;
                    normalized_components.push(v) ;
                }
                
            }) ;
            key = [collect, client, source, id ]  ;
            val[id] = normalized_components  ; 
            emit( key, { "appliance-management" : val, "svt_action":"svt_group", "svt_marked": id  } );
        
        // map all other 
        } else {
            key = [collect, client, source, id ]  ;
            val[id] = doc ;
            emit( key, {"appliance-management" : val, "svt_action":"svt_group" } );
        
        }
    }
}
