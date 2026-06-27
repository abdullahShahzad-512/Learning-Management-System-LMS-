class LMSCKEditor {

    static editors = {};

    static async init(id) {

        const element = document.getElementById(id);

        if (!element)
             return;

        const editor = await ClassicEditor.create(element, {

            toolbar: [

                "heading",

                "|",

                "bold",
                "italic",
                "underline",

                "|",

                "bulletedList",
                "numberedList",

                "|",

                "outdent",
                "indent",

                "|",

                "insertTable",

                "|",

                "blockQuote",

                "|",
                
                "codeBlock",

                "|",

                "undo",
                "redo"

            ]

        });

        LMSCKEditor.editors[id] = editor;

    }


    static getData(id) {

        return LMSCKEditor.editors[id].getData();

    }

    static setData(id, data) {

        LMSCKEditor.editors[id].setData(data);
    }

}
window.LMSCKEditor = LMSCKEditor;