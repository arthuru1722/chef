const form = document.querySelector("#contract-form");
const preview = document.querySelector("#preview");
const materialCount = document.querySelector("#material-count");
const materials = document.querySelector("#materials");
const draftStatus = document.querySelector("#draft-status");
const imageModeFields = form?.querySelectorAll("[name='image_mode']") || [];
const existingImage = form?.querySelector("[name='existing_image']");
const newImage = form?.querySelector("[name='new_image']");
const imagePreviewWrap = document.querySelector("#image-preview-wrap");
const imagePreview = document.querySelector("#image-preview");
const contractId = form?.querySelector("[name='contract_id']")?.value || "new";
const draftKey = `cheffy-contract-draft-${contractId}`;
let uploadedImageUrl = "";

function getFormData() {
    const data = {};
    const formData = new FormData(form);
    for (const [key, value] of formData.entries()) {
        if (key !== "new_image") {
            data[key] = value;
        }
    }
    data.autorizaImagem = form.querySelector("[name='autorizaImagem']")?.checked || false;
    data.materiais = [];
    const count = Number(materialCount.value || 0);
    for (let index = 0; index < count; index += 1) {
        data.materiais.push({
            nome: data[`material_nome_${index}`] || "",
            custo: data[`material_custo_${index}`] || "",
        });
    }
    return data;
}

function escapeHtml(value) {
    return String(value || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function fill(value, placeholder = "________") {
    return escapeHtml(value || placeholder);
}

function renderPreview() {
    const v = getFormData();
    const materialLines = v.materiais
        .map((item, index) => `${index + 1}) ${fill(item.nome)} Custo de reposicao: R$ ${fill(item.custo)}`)
        .join("<br>");

    preview.innerHTML = `
        <h3>CONTRATO DE PRESTACAO DE SERVICOS DE BUFFET</h3>
        <p><strong>IDENTIFICACAO DAS PARTES CONTRATANTES:</strong></p>
        <p><strong>Contratante:</strong> ${fill(v.nomeContratante)} Nacionalidade ${fill(v.nacionalidadeContratante)} Estado Civil ${fill(v.estadoCivilContratante)}, Profissao ${fill(v.profissaoContratante)}, Carteira de Identidade n° ${fill(v.rgContratante)}, C.P.F/CNPJ nº ${fill(v.cpfContratante)}, localizado na Rua ${fill(v.ruaContratante)}, nº ${fill(v.numeroContratante)}, bairro ${fill(v.bairroContratante)}, Cep ${fill(v.cepContratante)}, Cidade ${fill(v.cidadeContratante)}, no Estado ${fill(v.estadoContratante)};</p>
        <p><strong>Contratada:</strong> Ivanilda Caetano da Silva Santos CNPJ nº 62.114.618/0001-30, localizado na Rua Alameda Euridice Placido de Araujo Ivo, nº 15, bairro J. Petropolis II, Cep 57062-090, Cidade Maceio, no Estado AL;</p>
        <p>As partes acima identificadas tem, entre si, justo e acertado o presente Contrato de Prestacao de Servicos de Buffet, que se regera pelas clausulas seguintes e pelas condicoes de preco, forma e termo de pagamento descritas no presente.</p>
        <p><strong>Clausula 1a.</strong> E objeto do presente contrato a prestacao pela CONTRATADA a CONTRATANTE dos servicos de Buffet, em evento que se realizara na data de ${fill(v.diaEvento, "__")}/${fill(v.mesEvento, "__")}/${fill(v.anoEvento, "____")}, as ${fill(v.horaEvento, "__")}:${fill(v.minutoEvento, "__")} horas, no salao de festas situado na Rua ${fill(v.ruaEvento)}, nº ${fill(v.numeroEvento)}, bairro ${fill(v.bairroEvento)}, Cep ${fill(v.cepEvento)}, Cidade ${fill(v.cidadeEvento)}, no Estado ${fill(v.estadoEvento)};</p>
        <p><strong>Clausula 2a.</strong> O evento, para cuja realizacao sao contratados os servicos de buffet, e um(a) ${fill(v.tipoEvento)}, e contara com a presenca de ${fill(v.qtdPessoas, "___")} pessoas.</p>
        <p><strong>Clausula 3a.</strong> A CONTRATANTE devera fornecer a CONTRATADA todas as informacoes necessarias a realizacao adequada do servico de buffet, devendo especificar os detalhes do evento, necessarios ao perfeito fornecimento do servico, e a forma como este devera ser prestado.</p>
        <p><strong>Clausula 4a.</strong> E dever da CONTRATADA oferecer um servico de buffet de acordo com as especificacoes da CONTRATANTE, devendo o servico iniciar-se as ${fill(v.inicioHora, "__")}:${fill(v.inicioMinuto, "__")} horas e terminar as ${fill(v.terminoHora, "__")}:${fill(v.terminoMinuto, "__")} horas.</p>
        <p><strong>Clausula 5a.</strong> A CONTRATADA sera responsavel pela organizacao do local do evento, fornecendo os seguintes materiais necessarios para o melhor desempenho da prestacao do servico de Buffet:</p>
        <p>${materialLines}</p>
        <p><strong>Clausula 6a.</strong> A CONTRATADA compromete-se a chegar no local do evento as ${fill(v.chegadaHora, "__")}:${fill(v.chegadaMinuto, "__")} horas, a fim de arrumar o local do evento com antecedencia de ${fill(v.antecedenciaHoras, "__")} horas.</p>
        <p><strong>Clausula 7a.</strong> A CONTRATADA se compromete a fornecer o cardapio escolhido pela CONTRATANTE, cujas especificacoes, inclusive de quantidade a ser servida, encontram-se em documento anexo ao final deste presente contrato, passando a integrar-lhe.</p>
        <p><strong>Clausula 8a.</strong> A CONTRATADA fornecera ${fill(v.qtdGarcons, "__")} garcons e ${fill(v.qtdCopeiros, "__")} copeiros para a prestacao dos servicos ora contratados.</p>
        <p><strong>Clausula 9a.</strong> A CONTRATADA sera a unica e exclusiva responsavel por todos os seus funcionarios que trabalharem no evento referido na clausula 2a, cabendo a ela o cumprimento das obrigacoes trabalhistas entre outras.</p>
        <p><strong>Clausula 10a.</strong> E dever da CONTRATADA manter todos os seus funcionarios devidamente uniformizados durante a prestacao dos servicos ora contratados, garantindo que todos eles possuam os requisitos de urbanidade, moralidade e educacao.<br><br>Paragrafo unico. Caso algum funcionario seja afastado a pedido do CONTRATANTE, fica a criterio da CONTRATADA substitui-lo ou nao por outro, sem gerar multa ou danos a CONTRATADA.</p>
        <p><strong>Clausula 11a.</strong> O servico contratado no presente instrumento sera remunerado pela quantia de R$ ${fill(v.valorTotalNumero)} (${fill(v.valorTotalExtenso)}).<br><br>Paragrafo 1. O pagamento sera realizado via ${fill(v.tipoPagamento)}, parcelado em 2 vezes.<br>1a parcela - R$ ${fill(v.parcela1Numero)} (${fill(v.parcela1Extenso)}) em ${fill(v.parcela1Dia, "__")}/${fill(v.parcela1Mes, "__")}/${fill(v.parcela1Ano, "____")}<br>2a parcela - R$ ${fill(v.parcela2Numero)} (${fill(v.parcela2Extenso)}) em ${fill(v.parcela2Dia, "__")}/${fill(v.parcela2Mes, "__")}/${fill(v.parcela2Ano, "____")}.</p>
        <p>Paragrafo 2. Em caso de desistencia por parte da CONTRATANTE, nao sera concedido reembolso dos valores ja pagos, visto que tais valores sao retidos para cobrir custos administrativos e logisticos incorridos pela CONTRATADA devido a desistencia.<br><br>Paragrafo 3. Mesmo nos casos previstos no Paragrafo 2o desta clausula, a CONTRATANTE podera usar os valores ja pagos como credito para um novo agendamento, pelo prazo maximo de 6 meses a partir da data do cancelamento, desde que haja disponibilidade na agenda da CONTRATADA e que a solicitacao seja feita com antecedencia minima de ${fill(v.antecedenciaCredito, "__")} dias.</p>
        <p><strong>Clausula 12a.</strong> Em caso de inadimplemento por parte do CONTRATANTE quanto ao pagamento do servico prestado, devera incidir sobre o valor do presente instrumento multa pecuniaria de 2%, juros de mora de 1% ao mes e correcao monetaria.<br><br>Paragrafo unico. Em caso de cobranca judicial, devem ser acrescidas custas processuais e 30% de honorarios advocaticios.</p>
        <p><strong>Clausula 13a.</strong> Todos os utensilios e objetos fornecidos pela CONTRATADA, cujo a lista encontra-se na clausula 5, deverao ser devolvidos em perfeito estado de conservacao, sob pena da CONTRATANTE arcar com os respectivos custos de substituicao mencionados na clausula 5.</p>
        <p><strong>Clausula 14a.</strong> A CONTRATANTE assume a responsabilidade de cobrir os custos de substituicao dos itens danificados ou perdidos durante o evento, com a obrigacao de efetuar o pagamento ao termino do evento.</p>
        <p><strong>Clausula 15a.</strong> Caso a parte CONTRATANTE opte pela desistencia, sera necessario um aviso formal por escrito, ocorrendo com pelo menos ${fill(v.antecedenciaDesistencia, "__")} dias corridos de antecedencia em relacao a data prevista para o evento.</p>
        <p><strong>Clausula 16a.</strong> O cardapio foi elaborado de acordo com o numero de convidados determinado pela CONTRATANTE.<br><br>Paragrafo 1. Na hipotese de exceder o numero de convidados, a CONTRATANTE compromete-se a pagar uma taxa de R$ ${fill(v.valorExtraNumero, "___")} para cada novo convidado.<br><br>Paragrafo 2. No caso do excesso de convidados, a CONTRATADA nao sera responsabilizada se atendidas as especificacoes, ocorrer a insuficiencia da comida e/ou da bebida devido a esse excesso de pessoas.</p>
        <p><strong>Clausula 17a.</strong> O CONTRATANTE [AUTORIZA / NAO AUTORIZA] o uso de imagens do evento, para divulgacao em site, mostruarios, portfolios e anuncios comerciais, respeitando-se a integridade e a moralidade do CONTRATANTE.<br><br>(${v.autorizaImagem ? "X" : " "}) Sim, autorizo a divulgacao de imagem<br>(${v.autorizaImagem ? " " : "X"}) Nao autorizo a divulgacao de imagem<br><br>Fotos e Filmagens por conta do cliente, mas a empresa passara o contato se houver interesse.</p>
        <p><strong>Clausula 18a.</strong> Qualquer alteracao, modificacao, complementacao, ou ajuste, somente sera reconhecido e produzira efeitos legais, se incorporado ao presente contrato mediante Termo Aditivo, devidamente assinado pelas partes contratantes.</p>
        <p><strong>DO FORO</strong><br><br>Para dirimir quaisquer controversias oriundas do presente contrato, as partes elegem o foro da comarca da cidade de ${fill(v.cidadeForo)}; Por estarem assim justos e contratados, firmam o presente instrumento.</p>
        <p><strong>Contratante:</strong><br>Nome: ${fill(v.nomeContratante)}<br>Assinatura: ________________________________</p>
        <p><strong>Contratada:</strong><br>Nome: Ivanilda Caetano da Silva Santos<br>Assinatura: ________________________________</p>
        <p class="center">${fill(v.cidadeForo)}, ${fill(v.dataFinalDia, "__")} de ${fill(v.dataFinalMesExtenso, "________")} de 202${fill(v.dataFinalAnoUltimoDigito, "_")}.</p>
        ${v.image_mode === "none" ? "" : "<p><strong>Anexo</strong><br>Anexo contendo as especificacoes sobre o tipo e a quantidade de alimentos que serao fornecidos no evento, de acordo com o disposto na 7a Clausula.</p>"}
    `;
}

function currentImageMode() {
    return form.querySelector("[name='image_mode']:checked")?.value || "none";
}

function imageUrlFromProjectPath(path) {
    if (!path) {
        return "";
    }
    if (path.startsWith("path:")) {
        return `/${path.replace(/^path:/, "")}`;
    }
    if (path.startsWith("db:")) {
        return `/uploaded-images/${path.replace(/^db:/, "")}`;
    }
    return `/${path.replace(/^images\//, "images/")}`;
}

function updateImagePreview() {
    const mode = currentImageMode();
    let src = "";

    if (mode === "existing") {
        const selectedOption = existingImage?.selectedOptions?.[0];
        src = selectedOption?.dataset?.url || imageUrlFromProjectPath(existingImage?.value || "");
    }

    if (mode === "upload" && newImage?.files?.[0]) {
        if (uploadedImageUrl) {
            URL.revokeObjectURL(uploadedImageUrl);
        }
        uploadedImageUrl = URL.createObjectURL(newImage.files[0]);
        src = uploadedImageUrl;
    }

    if (src) {
        imagePreview.src = src;
        imagePreviewWrap.classList.add("has-image");
    } else {
        imagePreview.removeAttribute("src");
        imagePreviewWrap.classList.remove("has-image");
    }
}

function saveDraft() {
    localStorage.setItem(draftKey, JSON.stringify(getFormData()));
    draftStatus.textContent = "Rascunho salvo neste navegador";
}

function restoreDraft() {
    if (contractId !== "new") {
        return;
    }
    const rawDraft = localStorage.getItem(draftKey);
    if (!rawDraft) {
        return;
    }
    const data = JSON.parse(rawDraft);
    for (const [key, value] of Object.entries(data)) {
        const field = form.elements[key];
        if (!field || key === "materiais") {
            continue;
        }
        if (field.type === "checkbox") {
            field.checked = Boolean(value);
        } else {
            field.value = value;
        }
    }
    if (Array.isArray(data.materiais)) {
        data.materiais.forEach((item, index) => {
            ensureMaterialRow(index);
            const nome = form.elements[`material_nome_${index}`];
            const custo = form.elements[`material_custo_${index}`];
            if (nome) nome.value = item.nome || "";
            if (custo) custo.value = item.custo || "";
        });
    }
}

function ensureMaterialRow(index) {
    while (Number(materialCount.value) <= index) {
        addMaterialRow();
    }
}

function addMaterialRow() {
    const index = Number(materialCount.value || 0);
    const row = document.createElement("div");
    row.className = "material-row";
    row.innerHTML = `
        <label>
            <span>Material</span>
            <input name="material_nome_${index}" autocomplete="off">
        </label>
        <label>
            <span>Custo de reposicao</span>
            <input name="material_custo_${index}" autocomplete="off">
        </label>
    `;
    materials.appendChild(row);
    materialCount.value = String(index + 1);
}

document.querySelector("#add-material")?.addEventListener("click", () => {
    addMaterialRow();
    renderPreview();
    saveDraft();
});

document.querySelector("#clear-draft")?.addEventListener("click", () => {
    const message = contractId === "new"
        ? "Limpar o rascunho deste contrato novo?"
        : "Limpar alteracoes nao salvas deste contrato e recarregar os dados salvos?";
    if (!window.confirm(message)) {
        return;
    }
    localStorage.removeItem(draftKey);
    window.location.reload();
});

document.querySelectorAll(".delete-contract-form").forEach((deleteForm) => {
    deleteForm.addEventListener("submit", (event) => {
        const title = deleteForm.dataset.contractTitle || "este contrato";
        if (!window.confirm(`Excluir ${title}? Essa acao nao pode ser desfeita.`)) {
            event.preventDefault();
        }
    });
});

form?.addEventListener("input", () => {
    renderPreview();
    saveDraft();
});

form?.addEventListener("change", () => {
    renderPreview();
    updateImagePreview();
    saveDraft();
});

form?.addEventListener("submit", () => {
    localStorage.removeItem(draftKey);
});

restoreDraft();
renderPreview();
updateImagePreview();
saveDraft();
