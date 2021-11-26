close all;
clear all;
img = imread('image.jpg');
img = rgb2gray(img);

[row,column]= size(img);
imzero = zeros(row+2,column+2);
imzero(2:row+1,2:column+1) = img;
img = imzero;
[row,column]= size(img);
im_v = zeros(size(img));
im_h = zeros(size(img));
x = row - 3;
y = column -3;
for i = 1 : x
    for j = 1 : y
        p =  img(i:i+2,j:j+2);
        im_v(i+1,j+1) = Prewitt_V(p);
        im_h(i+1,j+1) = Prewitt_H(p);
    end
end
img  = uint8(img);
im_v = uint8(im_v);
im_h = uint8(im_h);

figure,imshow(img);
figure,imshow(im_v);
figure,imshow(im_h);

im_new = im_v + im_h;
figure,imshow(im_new);



        
