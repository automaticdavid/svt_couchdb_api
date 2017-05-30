// view for vro docs
// returns plugins sub-jsons


function(doc) {

    var key ;
    var normalized_plugins = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vro_plugins") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        plugins = doc.plugin ;
        
        count = 1 ;
        plugins.forEach(function(plugin) {
            var v = {} ;
            v.svt_unic = "plugin"+count ;
            v.svt_value = plugin ;
            normalized_plugins.push(v) ;
            count++;

            } 
        ) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"plugins":normalized_plugins, "svt_action":"svt_single"} );

    }
}


