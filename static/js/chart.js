let state = null;
let disease = null;
let estadoSaude = 1;
let url = window.location.origin;
let chartCanvas = document.getElementById("myChart");

function lineChart(vals,datas){
    let data = [{
        label: "Covid",
        data: vals,
        lineTension: 0,
        fill: false,
        borderColor: 'red'
    }];

    let speedData = {
      labels: datas,
      datasets: data
    };

    let chartOptions = {
      legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        }
      }
    };

    let lineChart = new Chart(chartCanvas, {
      type: 'line',
      data: speedData,
      options: chartOptions
    });
}

let initSelect = () => {
    jQuery('.changeSelect').change((el) => {
        let val = el.target.value == 0 ? null : el.target.value;
        let id = jQuery(el.target).attr('id');
        if(id === 'state'){
            state = val
        }else{
            disease = val
        }
        request()
    })
};

let request = () => {
    jQuery.ajax({
        url : `${url}/report`,
        type : 'POST',
        data : {
            state,
            disease,
            estadoSaude
        },
        success : function(data) {
            let vals = [];
            let datas = [];
            for(let d of data){
                vals.push(parseFloat(d.total));
                let date = new Date(d.data);
                datas.push(`${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`);
            }
            lineChart(vals, datas);
        },
        error : function(xhr, textStatus, errorThrown ) {
            console.log(xhr);
        }
    });
};

jQuery(document).ready(function(){
    initSelect();
    request();
});