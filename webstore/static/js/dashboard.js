 $(function(){
                $.ajax({
                    url: '/getItems',
                    type: 'GET',
                    success:function(response) {
                    console.log(response);
                    var data = JSON.parse(response);
                    var itemsPerRow = 0;
                    var div = $('<div>').attr('class','row marketing');
                    for(var i=0;i<data.length;i++){
                        console.log(data[i].Title);
                        
                        
                        if(itemsPerRow<3){
                            console.log(i);
                            if(i==data.length-1){
                                div.append(CreateThumb(data[i].Id,data[i].Title,data[i].Description,data[i].FilePath));
                                $('.well').append(div);
                            }
                            else{
                            div.append(CreateThumb(data[i].Id,data[i].Title,data[i].Description,data[i].FilePath));
                            itemsPerRow++;
                            }
                        }
                        else{
                            $('.well').append(div);
                            div = $('<div>').attr('class','row');
                            div.append(CreateThumb(data[i].Id,data[i].Title,data[i].Description,data[i].FilePath));
                            if(i==data.length-1){
                                $('.well').append(div);
                            }
                            itemsPerRow = 0;
                        }
                    }
                    
                    },
                    error:function(error){
                        console.log(error);
                    }
                });

            });

                function CreateThumb(id,title,desc,filepath){
                    var mainDiv = $('<div>').attr('class','col-lg-6');
                    var thumbNail = $('<div>').attr({'class':'card','style':'width: 18rem'});
                    var img = $('<img>').attr({'src':filepath,'data-holder-rendered':true,'class':'card-img-top','alt':'...'});
                    var caption = $('<div>').attr('class','card-body');
                    var title = $('<h5>').attr('class','card-title').text(title);
                    var desc = $('<p>').attr('class','card-text').text(desc);
                    
                    var p = $('<p>');
                    var btn = $('<button>').attr({'id':'btn_'+id,'type':'button','class':'btn btn-outline-warning'});
                   var span = $('<span>').attr({
                        'class': 'glyphicon glyphicon-thumbs-up',
                        'aria-hidden': 'true'
                    }).text('Buy');
                    
                    
                    p.append(btn.append(span));
                    
                    
                    caption.append(title);
                    caption.append(desc);
                    caption.append(p);
                    thumbNail.append(img);
                    thumbNail.append(caption);
                    mainDiv.append(thumbNail);
                    return mainDiv;
                    
                }
        


