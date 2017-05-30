// view for vro docs
// returns workflows sub-jsons


function(doc) {

    var key ;
    var normalized_workflows = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vro_workflows") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        workflows = doc.link ;

        count = 1;
        workflows.forEach(function(workflow) {
            var v = {} ;
            v.svt_unic = "workflow"+count ;
            v.svt_value = workflow ;
            normalized_workflows.push(v) ;
            count++;
            }
        ) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"workflows":normalized_workflows, "svt_action":"svt_single"} );

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

