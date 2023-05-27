import axios from 'axios';

let base = 'http://127.0.0.1:5000/api';

// 超级管理员页面的api-----------------------------------------
export const requestAdminLogin = params => {
    return axios({
        method: 'POST',
        url: `${base}/adminLogin`,
        auth: params
    })
    .then(res => res.data);
};

export const adminSetpwd = params => {
    return axios.post(`${base}/adminSetpwd`, params);
};

export const getUserList = params => {
    return axios.get(`${base}/adminGetUserList`, { params: params });
};

export const setUserPermit = params => {
  return axios.get(`${base}/adminSetUserList`, { params: params });
};

export const removeUser = params => {
    return axios.get(`${base}/adminUserRemove`, { params: params });
};

export const batchRemoveUser = params => {
    return axios.get(`${base}/adminBatchRemove`, { params: params });
};

export const getDomainList = params => {
  return axios.get(`${base}/getDomainList`, { params: params });
};

export const addDomainList = params => {
  return axios.get(`${base}/adminAddDomainList`, { params: params });
};

export const deleteDomainList = params => {
  return axios.get(`${base}/adiminDeleteDomainList`, { params: params });
};

export const updateDomain = params => {
  return axios.get(`${base}/adminUpdateDomain`, { params: params });
};

export const paperView = params => {
  return axios.get(`${base}/paperView`, { params: params });
};

// 普通用户页面的api----------------------------------------
export const requestLogin = params => {
    return axios({
        method: 'POST',
        url: `${base}/login`,
        auth: params
    })
    .then(res => res.data);
};

export const requestRegister = params => {
    return axios.post(`${base}/register`, params);
};

export const nameNoRepeat = params => {
    return axios.post(`${base}/nameNoRepeat`, params);
};

export const getVerifyCode = params => {
    return axios.post(`${base}/getVerifyCode`, params);
};

export const getMyPaperList = params => {
    return axios.get(`${base}/myPaperList`,{ params: params });
}

export const getPaperList = params => {
    return axios.get(`${base}/getPaperList`, {params})
};

export const publishPaper = params => {
  return axios.get(`${base}/publishPaper`, { params: params });
}

export const getPaperListByTitles = params => {
    return axios.get(`${base}/getPaperListByTitles`, {params})
};

export const getNoteList = params => {
    return axios.get(`${base}/getNoteList`, {params})
}

export const updatePaper = params => {
  return axios.get(`${base}/updatePaper`, { params: params} );
}

export const addNote = params => {
    return axios.get(`${base}/addNote`, {params})
}


export const deletePaper = params => {
  return axios.get(`${base}/deletePaper`, { params: params} );
}

export const canIAddNote = params => {
    return axios.get(`${base}/canIAddNote`, {params})
}

// 文件上传相关
export const uploadFile = params => {
  return axios.post(`${base}/receiveAFile`, params);
}

export const getFile = params => {
  return axios.get(`${base}/getAFile`, { params: params} );
}

export const getdrawPieChart = params => {
  return axios.get(`${base}/getDrawPieChart`, { params: params} );
}

export const adminDrawPieChart = params => {
  return axios.get(`${base}/adminDrawPieChart`, { params: params} );
}

export const getCommentList = params => {
    return axios.get(`${base}/getCommentList`, { params: params} );
}

export const addComment = params => {
    return axios.get(`${base}/addComment`, { params: params} );
}

export const addReply = params => {
    return axios.get(`${base}/addReply`, { params: params} );
}

export const deleteReply = params => {
    return axios.get(`${base}/deleteReply`, { params: params} );
}

export const deleteComment = params => {
    return axios.get(`${base}/deleteComment`, { params: params} );
}

export const deleteNote = params => {
    return axios.get(`${base}/deleteNote`, { params: params} );
}

export const adminDeletePaper = params => {
    return axios.get(`${base}/adminDeletePaper`, { params: params} );
}