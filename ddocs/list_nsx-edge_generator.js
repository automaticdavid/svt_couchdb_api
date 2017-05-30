// generator list function

function(head, req) {

    provides('json', function() {

        var row = getRow();
        if (!row){
            var j = {'svt_nodata':'svt_nodata'} ;
        }    

        var j = {};
        while(row=getRow()){

            [collect, client, source, id] = row.key ;
            j[source]=j[source] || {} ;
            log(row.key) ; 

            o = row.value ;

            if (o.svt_action === "svt_standard" || o.svt_action == "svt_multi") {

                delete o.svt_action ; 
                s = Object.keys(o)[0] ;
                p = o[s] ;

                if (Array.isArray(p)) {
   
                    p.forEach(function(i){
                        u = i.svt_unic ;
                        v = i.svt_value ;
                        j[source][id]=j[source][id] || {} ;
                        j[source][id][u] = v ;
                    });

                } else {
                    j[source][id] = row.value ;
                }

            }

        
        }

        send(JSON.stringify(j));

    });
}
