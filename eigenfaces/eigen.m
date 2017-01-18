start_index = 1;
end_index   = 6;
base_name   = '';
extension   = '.jpg';
in_dir      = 'cameron';
out_dir     = 'david';

images = [];

%read each image, store it as a row vector, and store all those
%vectors as rows of the images matrix:
for i=start_index:end_index
    img = imread(strcat(in_dir, '/', base_name, num2str(i), extension));
    img = double(rgb2gray(img));
    [rows cols] = size(img);
    img = img(:)';
    images = vertcat(images, img);
end

images_mean = mean(images);
images = images - ones(end_index - start_index + 1, 1) * images_mean;

%perform PCA on 'images':
[C, S, L] = princomp(images, 'econ');

%save the eigenvectors as images:
for i=1:size(C,2)
    img = C(:,i);
    img = reshape(img,rows,cols);
    img = ( img - min(img(:)) ) ./ ( max(img(:)) - min(img(:)) );
    imwrite(img, strcat(out_dir, '/', num2str(i), extension));
end