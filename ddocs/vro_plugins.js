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
            && doc.plugin
        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        plugins = doc.plugin ; 
        if (doc.total) {
            total = doc.total ;
        } else {
            total = 'svt_no_data';
        } ;
        
        // loop the plugins
        plugins.forEach(function(plugin) {
            var v = {} ;
            if (plugin.moduleName) {
                v.svt_unic = plugin.moduleName ;
                var enrich = {"TotalNumberOfPlugins":total} ;
                v.svt_value = Concat(plugin, enrich) ;
                normalized_plugins.push(v) ;
            } 
        }) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"plugins":normalized_plugins, "svt_action":"svt_single"} );

    }
}

function Concat(a, b) {
    var c = {};
    for (var i in a)
        c[i] = a[i] ;
    for (var j in b)
        c[j] = b[j] ;
    return c;
}

