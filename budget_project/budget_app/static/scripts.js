var mini = true;

        function toggleSidebar() {
            if (mini) {
                console.log("opening sidebar");
                document.getElementById("mySidebar").style.width = "250px";
                document.getElementById("main").style.marginLeft = "250px";
                this.mini = false;
            } else {
                console.log("closing sidebar");
                document.getElementById("mySidebar").style.width = "85px";
                document.getElementById("main").style.marginLeft = "85px";
                this.mini = true;
            }
        }
document.addEventListener('DOMContentLoaded', function() {
                var elemss = document.querySelectorAll('select');
                var instancess = M.FormSelect.init(elemss);
                var elems = document.querySelectorAll('.datepicker');
                var instances = M.Datepicker.init(elems, {
                format:'yyyy-mm-dd',
                autoClose: true,
                defaultDate: new Date(),
                setDefaultDate: true});

            });