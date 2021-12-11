const parseDate = (date) => {
    // Esto iria en un utils
    return date.split(' ')[0]

}

export const getArchiveCasesDistributedByDate = (tasks) => {
    const distributionByDate = {}
    tasks.forEach((task) => distributionByDate[parseDate(task.end_date)] = distributionByDate[parseDate(task.end_date)]++ || 1 )
    return distributionByDate
}
    
