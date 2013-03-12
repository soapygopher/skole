% read from file into 20x20x3 matrix
rgbimg = imread('./images/image1_a.png', 'png');

% reshape colors to 400x1 matrices
reds = reshape(rgbimg(:,:,1), 400, 1);
greens = reshape(rgbimg(:,:,2), 400, 1);
blues = reshape(rgbimg(:,:,3), 400, 1);

% x and y indices
xs = repmat((1:20)', 20, 1);
ys = [];
for i = 1:20
    ys = [ys; ones(20, 1) * i];
end

% concatenate to 400x5 matrix of [r, g, b, x, y] values
rgbxy = [reds, greens, blues, xs, ys];
rgbxy

