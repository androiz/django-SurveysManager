/**
 * Created by Andres on 9/1/17.
 */

var q = '<div class="question question_#nn"> <div class="row control-group">' +
                '<div class="form-group col-xs-2"><h2>##nn</h2></div> ' +
                '<div class="form-group col-xs-10 controls"> ' +
                '<label for="sel1">Question Type:</label> ' +
                '<select class="form-control question_type question_type_#nn"> ' +
                '<option value="text">Text</option> ' +
                '<option value="integer">Integer</option> ' +
                '<option value="checkbox">Checkbox</option> ' +
                '<option value="select">Select</option> ' +
                '</select> ' +
                '</div> ' +
                '</div> ' +
                '<div class="row control-group"> ' +
                '<div class="form-group col-xs-2"></div> ' +
                '<div class="form-group col-xs-10 controls"> ' +
                '<label>Description:</label> ' +
                '<textarea class="form-control question_description" rows="3"></textarea> ' +
                '</div> ' +
                '</div> ' +
                '<div class="row control-group question_options_#nn"> ' +
                '<div class="form-group col-xs-2"></div> ' +
                '<div class="form-group col-xs-10 controls"> ' +
                '<div class="alert alert-info" role="alert">' +
                'Please, write all options separated by <strong>comma (,)</strong> if you are' +
                'setting up a <strong>select</strong> or <strong>checkbox</strong> widget. ' +
                '</div> ' +
                '<label>Options:</label> ' +
                '<input type="text" class="form-control question_options"> ' +
                '</div> ' +
                '</div> ' +
                '</div>';

$("#add_question").click(function () {
    var n = $('.question').length;
    var new_question = q.replace(/#nn/g, n+1);
    $(".question").last().after(new_question);
});
$("#remove_question").click(function () {
    var n = $('.question').length;
    if (n > 1){
        $('.question').last().remove();
    }
});