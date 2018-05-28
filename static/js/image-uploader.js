App.ImageUploader = {

    CLASS_NAME_UPLOADER: 'js-avatar-uploader',
    CLASS_NAME_FILE_FIELD: 'js-avatar-uploader--file-field',
    CLASS_NAME_IMAGE: 'js-avatar-uploader--image',

    UPLOAD_FILE_SIZE_LIMIT: 5000000,  // Size in Bytes - 5MB.
    UPLOAD_FILE_MIN_DIMENSIONS: 250,
    UPLOAD_FILE_ALLOWED_MIMES: ['image/jpeg', 'image/png'],


    registerEvents: function(){

        $('.' + this.CLASS_NAME_FILE_FIELD).on('change', function(event){

            var previewImage = $('.' + App.ImageUploader.CLASS_NAME_IMAGE);

            if (this.files.length === 0) {
                previewImage.attr('src', previewImage.data('default-srx'));
                return;
            }

            var file = this.files[0];

            if(file.size > App.ImageUploader.UPLOAD_FILE_SIZE_LIMIT) {

                var sizeMB = String(App.ImageUploader.UPLOAD_FILE_SIZE_LIMIT / 1000000);
                alert('Your file is too big. It must be smaller than ' + sizeMB + 'Mb.');
                return;
            }

            var fileHasCorrectMimeType = false;

            for(var i = App.ImageUploader.UPLOAD_FILE_ALLOWED_MIMES.length - 1; i >= 0; i--){

                if(App.ImageUploader.UPLOAD_FILE_ALLOWED_MIMES[i] === file.type){
                    fileHasCorrectMimeType = true;
                    break;
                }
            }

            if(!fileHasCorrectMimeType){
                alert('Only JPG and PNG formats are allowed.');
                return;
            }

            var reader  = new FileReader();
            reader.addEventListener('load', function (event) {
                var img = new Image();
                img.onload = function(){

                    var minDimension = App.ImageUploader.UPLOAD_FILE_MIN_DIMENSIONS;

                    if(this.naturalWidth < minDimension ||
                        this.naturalHeight < minDimension){
                        alert('Image must have dimensions at least ' + String(minDimension) + 'px x ' + String(minDimension) + 'px.');
                        return;
                    }
                    previewImage.attr('src', reader.result);

                };
                img.src = event.target.result;

            }, false);
            reader.readAsDataURL(file);

        });

    },
    init: function(){
        this.registerEvents();
    }
};
App.ImageUploader.init();
