function convv(img_path, kernel, stride, type)
    
    input= imread(img_path);
    
    n= length(input);
    f= length(kernel);
    
    if type== "same"
        p= floor((f - 1) / 2);
        o= ((n + 2 * p - f) + 1);
        input= padarray(input, [p, p], 0, 'both');
    else
        o= (n - f + 1);
        
    end    
    
    output= uint8(zeros(o, o));
    
    for c= 1:3
        for i= 1 : n - f + 1
            for j= 1 : n - f + 1
                window= input(i : i + f - 1, j : j + f - 1, c);
                s= uint8(sum(double(window) .* double(kernel), 'all'));
                
                output(i, j, c)= s;
              
            end
        end
    end
    
    imshow(output);
    
    
end
    
    

