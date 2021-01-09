
    //API  key 
    // AIzaSyBXzj_PXu3bNIJG_zj1N8oe-Td7DuJPH1Q
    // Client ID
    // 9560680490-445ms1tlt3mm5df3c24i3iqg9votuqe4.apps.googleusercontent.com
    // APP ID
    // 9560680490
    
    // The Browser API key obtained from the Google API Console.
    // Replace with your own Browser API key, or your own key.
    var developerKey = 'AIzaSyBXzj_PXu3bNIJG_zj1N8oe-Td7DuJPH1Q';

    // The Client ID obtained from the Google API Console. Replace with your own Client ID.
    var clientId = "9560680490-445ms1tlt3mm5df3c24i3iqg9votuqe4.apps.googleusercontent.com"

    // Replace with your own project number from console.developers.google.com.
    // See "Project number" under "IAM & Admin" > "Settings"
    var appId = "9560680490";

    // Scope to use to access user's Drive items.
    var scope = ['https://www.googleapis.com/auth/drive.file'];

    var pickerApiLoaded = false;
    var oauthToken;

    // Use the Google API Loader script to load the google.picker script.
    function loadPicker() {
      gapi.load('auth', {'callback': onAuthApiLoad});
      gapi.load('picker', {'callback': onPickerApiLoad});
    }

    function onAuthApiLoad() {
      window.gapi.auth.authorize(
          {
            'client_id': clientId,
            'scope': scope,
            'immediate': false
          },
          handleAuthResult);
    }

    function onPickerApiLoad() {
      pickerApiLoaded = true;
      createPicker();
    }

    function handleAuthResult(authResult) {
      if (authResult && !authResult.error) {
        oauthToken = authResult.access_token;
        createPicker();
      }
    }

    // Create and render a Picker object for searching images.
    function createPicker() {
      if (pickerApiLoaded && oauthToken) {
        var view = new google.picker.View(google.picker.ViewId.DOCS);
        view.setMimeTypes("image/png,image/jpeg,image/jpg");
        var picker = new google.picker.PickerBuilder()
            .enableFeature(google.picker.Feature.NAV_HIDDEN)
            .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
            .setAppId(appId)
            .setOAuthToken(oauthToken)
            .addView(view)
            .addView(new google.picker.DocsUploadView())
            .setDeveloperKey(developerKey)
            .setCallback(pickerCallback)
            .build();
         picker.setVisible(true);
      }
    }

    // A simple callback implementation.
    function pickerCallback(data) {
      if (data.action == google.picker.Action.PICKED) {
        var fileId = data.docs[0].id;
        var fileName = data.docs[0].name;
        var fileURL = data.docs[0].url;
        //alert('The user selected: ' + fileId);
        document.getElementById('id_name').value = fileName;
        document.getElementById('id_name_output').value = fileName;
        //document.getElementById('id_url').value = fileURL;
        document.getElementById('id_file_id').value = fileId;
      }
    }