$(document).ready(function() {
    $('#statuss').multiselect({
        buttonWidth: 170,
        nonSelectedText: 'Filter Status...'
    });

    $('#assignees').multiselect({
        enableFiltering: true,
        buttonWidth: 170,
        nonSelectedText: 'Filter Assignees...'
    });

    $(".caret").remove(); // because there are two caret otherwise

    function myFilter(){
        let $table = $("#tasks-table"),
            $rows = $table.find('tbody tr');

        /* Useful DOM data and selectors */
        let $searchtask = $("#searchtask"),
                $statuss = $("#statuss"),
                $assignee = $("#assignees"),
                $start_date_min = $("#start-date-min"),
                $start_date_max = $("#start-date-max"),
                $due_date_min = $("#due-date-min"),
                $due_date_max = $("#due-date-max");

        let inputTask = $searchtask.val().toLowerCase(),
                inputStatus = $statuss.val(),
                inputAssignee = $assignee.val(),
                inputStartDateMin = new Date($start_date_min.val()),
                inputStartDateMax = new Date($start_date_max.val()),
                inputDueDateMin = new Date($due_date_min.val()),
                inputDueDateMax = new Date($due_date_max.val());

        /* Filter function */
        let $filteredRows = $rows.filter(function(){
            let value = false;
            value |= ($(this).find('td').eq(1).text().toLowerCase().indexOf(inputTask) === -1);
            if (inputStatus.length!==0) {
                value |= (inputStatus.indexOf($(this).find('td').eq(2).text()) === -1);
                console.log(inputStatus.length);
             }
            if (inputAssignee.length!==0)
                value |= (inputAssignee.indexOf($(this).find('td').eq(3).text()) === -1);

            value |= ((new Date($(this).find('td').eq(4).text())) < inputStartDateMin);
            value |= ((new Date($(this).find('td').eq(4).text())) > inputStartDateMax);
            value |= ((new Date($(this).find('td').eq(5).text())) < inputDueDateMin);
            value |= ((new Date($(this).find('td').eq(5).text())) > inputDueDateMax);

            return value;
        });

        /* Clean previous no-result if exist */
        $table.find('tbody .no-result').remove();
        /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
        $rows.show();
        $filteredRows.hide();
        /* Prepend no-result row if all rows are filtered */
        if ($filteredRows.length === $rows.length) {
          $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="12">No tasks found</td></tr>'));
        }
    }
    $(".filters").keyup(myFilter);
    $(".filters").change(myFilter);


    $('#tasks-table').DataTable({
      "searching": false,
      "bPaginate": false,
      "bLengthChange": false,
      "bInfo": false,
      "bAutoWidth": false,
      "aoColumnDefs" : [
              {"bSortable" : false,
                "aTargets" : [ 6 ]},
              {"sType" : "rankStatus",
                "aTargets" : [ 2 ]},
              {"sType" : "rankDate",
                "aTargets" : [ 4, 5 ]},
      ],
    });


    jQuery.extend( jQuery.fn.dataTableExt.oSort, {
      "rankStatus-pre": function ( a ) {
        function getRankStatus(status) {
          let rankNumber;
          if (status === "Nouvelle"){
            rankNumber = 5;
          }
          else if (status === "En cours"){
            rankNumber = 4;
          }
          else if (status === "En attente") {
            rankNumber = 3;
          }
          else if (status === "Terminée") {
            rankNumber = 2;
          }
          else if (status === "Classée") {
            rankNumber = 1;
          }
          else {
            rankNumber = 0;
          }
          return rankNumber;
        }
        let res = a.split(">")[1].split("<")[0]; // 'a' de la forme "<h6 class="status">En attente</h6>"
        return getRankStatus(res); // 'res' de la forme "En attente"
      }
    });

    jQuery.extend( jQuery.fn.dataTableExt.oSort, {
      "rankDate-pre": function ( a ) {
        function getRankDate(date) {
          const months = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."];

          let parts = date.split(" ");

          let month = parts[0];
          if (month.length == 1)
            month = "0".concat('', month);
          let num = parts[1].split(",")[0];
          if (num.length == 1)
            num = "0".concat('', num);
          let year = parts[2];

          return parseInt(year.concat('', months.indexOf(month)).concat('',num), 10);
        }
        let res = a.split(">")[1].split("<")[0]; // 'a' de la forme "<h4 class="date">May 6, 2020</h4>"
        console.log(getRankDate(res))
        return getRankDate(res); // 'res' de la forme "May 6, 2020"
      }
    });
});