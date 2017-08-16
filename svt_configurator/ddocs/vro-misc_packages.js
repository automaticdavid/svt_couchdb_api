// view for vro docs
// returns packages sub-jsons


function(doc) {

    var key ;
    var normalized_packages = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vro_packages") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        packages = doc.link ;

        count = 1;
        packages.forEach(function(each_package) {
            var v = {} ;
            v.svt_unic = "package"+count ;
            v.svt_value = each_package
            normalized_packages.push(v) ;
            count++;
            }
        ) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"packages":normalized_packages, "svt_action":"svt_single"} );

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

