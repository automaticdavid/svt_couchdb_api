// view for vro docs
// returns rescources sub-jsons


function(doc) {

    var key ;
    var normalized_resources = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vro_resources") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        resources = doc.link

        count = 1;
        resources.forEach(function(resource) {
            var v = {} ;
            v.svt_unic = "resource"+count ;
            v.svt_value = resource ;
            normalized_resources.push(v) ;
            count++;
            }
        ) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"resources":normalized_resources, "svt_action":"svt_single"} );

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

