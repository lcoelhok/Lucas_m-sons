#include <memory>
#include <string>
#include <iostream>
#include <sstream>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"


#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "TTree.h"
#include "TH1.h"
#include "TLorentzVector.h"

using reco::GenParticleCollection;
using namespace std;
using namespace reco;
using namespace edm;

class GenLevelStudies : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
	public:
		explicit GenLevelStudies(const edm::ParameterSet&);
		~GenLevelStudies();

        
	private:
		virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
                virtual void beginJob() override ;
                virtual void endJob() override ;
                void initialize();
		// ----------member data ---------------------------
		edm::EDGetTokenT<GenParticleCollection> genParticlesToken_;
                TLorentzVector muon1, muon2, psi2S;
		TTree *mc;
		TH1D *psipt, *psieta;
		TH1D *dstarpt, *dstareta;

		vector<double> genpt;
        vector<double> geneta;
		int runNumber=0; int eventNumber=0;   

		vector<double> Psipt;
		vector<double> Psieta;

		vector<double> Dstarpt;
		vector<double> Dstareta;
              
};
GenLevelStudies::GenLevelStudies(const edm::ParameterSet& iConfig)
	:genParticlesToken_(consumes<GenParticleCollection>(edm::InputTag{"genParticles"}))
{
	//now do what ever initialization is needed
	edm::Service<TFileService> fs;
	mc = fs->make<TTree>("mc","mc");

	    TFileDirectory Mreconst = fs->mkdir("MrecoHist");

psipt = Mreconst.make<TH1D>("psipt", "Psi pT; p_{T} (GeV/c); Events", 100, 0, 100);
psieta = Mreconst.make<TH1D>("psieta", "Psi Eta; #eta; Events", 100, -2.7, 2.7);
dstarpt = Mreconst.make<TH1D>("dstarpt", "D* pT; p_{T} (GeV/c); Events", 100, 0, 100);
dstareta = Mreconst.make<TH1D>("dstareta", "D* Eta; #eta; Events", 100, -2.7, 2.7);

}


GenLevelStudies::~GenLevelStudies()
{

	// do anything here that needs to be done at desctruction time
	// (e.g. close files, deallocate resources etc.)

}

void
GenLevelStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	using namespace std;
    //to clear vectors
    initialize();
    //run, event, lumi section
	runNumber= iEvent.id().run();
	eventNumber= iEvent.id().event();

	Handle<GenParticleCollection> genParticles;
	iEvent.getByToken(genParticlesToken_, genParticles);
	cout << "Running " << endl;

        int cdstar = 0;
        for(const auto& genParticles : iEvent.get(genParticlesToken_) ){

        double pt = genParticles.pt();
        double eta = abs(genParticles.eta());


                if (genParticles.pdgId() == 413 && genParticles.numberOfDaughters()==2){

                        if ((genParticles.daughter(0)->pdgId() == 421) && (genParticles.daughter(1)->pdgId() == 211)){
                                //std::cout << genParticles.daughter(0)->daughter(0)->pdgId() << std::endl;
                                if ((genParticles.daughter(0)->daughter(0)->pdgId() == -321) && (genParticles.daughter(0)->daughter(1)->pdgId() == 211) ){

                                        dstarpt->Fill(genParticles.pt());
                                        dstareta->Fill(genParticles.eta());
                    
                                        cout << genParticles.pt() << endl;

                                      //  dstarvertexX->Fill(genParticles.vertex().x());
                                       // dstarvertexY->Fill(genParticles.vertex().y());
                                       // dstarvertexZ->Fill(genParticles.vertex().z());
                                        cdstar += 1;
}
}
}


                // fill vector
                genpt.push_back(pt);
                geneta.push_back(eta);



        }


mc->Fill();

}



    void GenLevelStudies::initialize( )
{
        runNumber=0; eventNumber=0;
        genpt.clear();
        geneta.clear();

}
///////
//++++++++++++++++++
void GenLevelStudies::endJob(){

    cout <<"######################################################################"<<endl;
    cout << "Number of Events: " << eventNumber << " Run Number: " << runNumber << endl;
    
}


/////////////////////
     void
GenLevelStudies::beginJob()
{
        mc->Branch("runNumber",&runNumber,"runNumber/I");
     	mc->Branch("eventNumber",&eventNumber,"eventNumber/I");
        mc->Branch("genpt",&genpt);
        mc->Branch("geneta",&geneta);
}

//////////////////////////////////////////
//define this as a plug-in
DEFINE_FWK_MODULE(GenLevelStudies);





