// view for nsx_edge docs
// returns appliances sub-jsons
// normalizes result with a unique key 


function(doc) {
    
    var key ; 
    var normalized = [] ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_edge") != -1
            && doc.appliances.appliances
            && doc.appliances.applianceSize
            && doc.appliances.deployAppliances
            && doc.id
        
        ) {
        
        // name the properties
        id = doc.id ;
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        appliances = doc.appliances.appliances ;
        size = doc.appliances.applianceSize ;
        deploy = doc.appliances.deployAppliances ;
        vmName = doc.appliances.appliances.vmName ;
        
        // loop the list
        appliances.forEach(function(appliance) {
            var v = {} ;
            v.svt_unic = appliance.vmName ;
            var enrich = {"applianceSize":size, "deployAppliances":deploy} ;
            v.svt_value =Concat(appliance, enrich) ;
            normalized.push(v) ; 
        }) ;

        // map all appliances   
        key = [collect, client, source, id]  ;
        emit( key,  {"appliances":normalized} );
        
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
