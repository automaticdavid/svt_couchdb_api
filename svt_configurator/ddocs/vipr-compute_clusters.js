function(doc) {
    
    var key ;
    var val = {} ; 
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_compute-cluster") != -1
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ; 
        elems = file.split("_").slice(-1) ;
        infos = elems.join("-") ; 
        id = infos.split(".")[0] ;
        label = file.split("_")[1].split("compute-cluster")[1].replace("-",'');
        if(label===''){label="cluster"}
        
        var lab = {};
        lab[label]=doc;
        
        key = [collect, client, source, id ]  ;

        if((id in val)){log(val[id]); val[id] = Concat(val[id],lab) ;} else { val[id]=lab;}

        emit( key, {"clusters" : val, "svt_action":"svt_group" } );
        
        
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